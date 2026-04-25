---
name: ai-chat-frontend
description: >
  アプリ組み込み AI チャットフロントエンドの設計・実装ガイド。
  前半は言語非依存の抽象設計パターン（ストリーミングファースト、チャット状態マシン、
  メッセージモデル、楽観的UI、エラーリカバリ、UX原則、マルチセッション、サーバー設計原則）、
  後半は Vercel AI SDK (useChat) による TypeScript 具体実装。
  フレームワーク非依存（Next.js, React SPA, Vue, Svelte, SvelteKit, Nuxt 対応）。
  Use when チャット機能を追加したい、AIチャットUIを作りたい、useChat を使いたい、
  ストリーミングチャットを実装したい、チャットボットUIを組み込みたい、
  AI SDK でチャットを作る、またはチャットUIの設計パターンを整理・レビューしたい時。
  Python/Go/Rust 等の非 TypeScript 環境でも設計パターン部分は適用可能。
  既存のチャットUIのレビュー・改善にも使える。
  対象外: チャット以外の AI SDK 用途（テキスト生成のみ、画像生成、エンベディング等）。
---

# AI Chat Frontend with Vercel AI SDK

Vercel AI SDK の `useChat` を軸に、アプリ組み込みチャットUIを設計・実装するガイド。
前半は言語・フレームワークに依存しない抽象設計パターン、後半は AI SDK による具体実装。

---

## 言語非依存: アプリ組み込みAIチャットの設計パターン

この章は Vercel AI SDK に限らず、任意の言語・フレームワークで AI チャットを組み込む際に適用できる普遍的な設計原則をまとめたもの。

### パターン1: ストリーミングファースト

LLM の応答は数秒〜数十秒かかる。一括返却だと体感待ち時間が長くなるため、**トークン単位の逐次表示（ストリーミング）をデフォルトにする**。

```
Client                     Server                    LLM
  │── POST /chat ──────────▶│                          │
  │                          │── prompt ──────────────▶│
  │◀── token₁ (SSE/WS) ─────│◀── token₁ ──────────────│
  │◀── token₂ ───────────────│◀── token₂ ──────────────│
  │◀── ...                   │◀── ...                  │
  │◀── [DONE] ───────────────│◀── finish ──────────────│
```

**トランスポート選択肢**:

| 方式 | 特徴 | 推奨場面 |
|------|------|----------|
| SSE (Server-Sent Events) | HTTP ベース、一方向、リトライ自動 | ほとんどのチャットUI（推奨） |
| WebSocket | 双方向、永続接続 | リアルタイム双方向通信が必要な場合 |
| Long Polling | 広い互換性 | レガシー環境のフォールバック |

SSE は HTTP/1.1 で6接続制限があるが、チャットUIでは通常1ストリームなので問題にならない。

### パターン2: チャット状態マシン

チャットの入力・送信・受信を**有限状態マシン**として設計すると、UI制御がシンプルになる。

```
         send()           first token        stream end
  READY ────────▶ SUBMITTED ────────▶ STREAMING ────────▶ READY
    ▲                                     │ stop()          ▲
    │                                     ▼                 │
    │                                  READY ───────────────┘
    │                error
    └────────────── ERROR (error 値は別途保持)
```

| 状態 | 入力欄 | 送信ボタン | 停止ボタン | 意味 |
|------|--------|-----------|-----------|------|
| READY | 有効 | 有効 | 非表示 | ユーザー入力待ち |
| SUBMITTED | 無効 | 無効 | 表示 | リクエスト送信済み、応答待ち |
| STREAMING | 無効 | 無効 | 表示 | トークン受信中 |
| ERROR | 有効 | 有効 | 非表示 | リトライボタンも表示 |

この状態マシンを守ることで**二重送信**や**ストリーミング中の操作不整合**を構造的に防止できる。

### パターン3: メッセージモデル

```
Message {
  id:        string          // 一意識別子（楽観的UIの key に使う）
  role:      "user" | "assistant" | "system"
  parts:     Part[]          // 構造化コンテンツ（テキスト、画像、ツール呼び出し等）
  createdAt: timestamp
  metadata?: Record<string, any>  // トークン使用量等の付加情報
}

Part {
  type: "text" | "image" | "tool-call" | "tool-result" | ...
  // type ごとのペイロード
}
```

**設計原則**:
- `content: string` ではなく `parts: Part[]` にする。テキスト以外（画像添付、ツール呼び出し結果）を後から拡張できる
- `id` はクライアント生成（UUID/ULID）。サーバー応答前でも楽観的に表示できる
- `role` で送信元を区別。UI の左右配置・色分けの根拠になる

### パターン4: 楽観的メッセージ追加

ユーザーが送信ボタンを押した瞬間に、サーバー応答を待たずメッセージリストに追加する。

```
1. ユーザー送信 → ローカルに user メッセージを即追加
2. 空の assistant メッセージを追加（ローディング表示用）
3. ストリームが到着するたびに assistant メッセージを差分更新
4. ストリーム完了で確定
```

これにより「送信した感」が即座に得られ、体感レイテンシが大幅に減る。

### パターン5: エラーリカバリ戦略

| エラー種別 | UI 対応 | 再試行方式 |
|-----------|---------|-----------|
| ネットワークエラー | 「接続できません」+ リトライ | 同じメッセージで再送 |
| サーバー 5xx | 「サーバーエラー」+ リトライ | 同じメッセージで再送 |
| レート制限 429 | 「しばらくお待ちください」 | 指数バックオフ付きリトライ |
| ストリーム途中断 | 受信済みテキストは保持 + リトライ | 最後の assistant メッセージを再生成 |
| コンテンツフィルタ | フィルタされた旨を表示 | 再試行は別のプロンプトで |

**鉄則**: エラー時に**受信済みのテキストを捨てない**。ユーザーが読んでいる可能性がある。

### パターン6: チャットUIのUX原則

| 原則 | 具体策 |
|------|--------|
| **自動スクロール** | 新メッセージ到着 / ストリーミング中に最下部を追従。ただしユーザーが上にスクロールしたら追従を止める |
| **Enter 送信 / Shift+Enter 改行** | textarea ベースの入力欄の標準挙動。モバイルでは送信ボタンのみ |
| **入力欄の動的リサイズ** | 入力テキスト量に応じて textarea を自動拡張（上限あり） |
| **ストリーミング中の視覚フィードバック** | カーソル点滅、typing indicator、部分テキストの逐次表示 |
| **空メッセージ送信防止** | `trim()` が空なら送信ボタンを無効化 |
| **コピー可能** | assistant の応答テキストをワンクリックでコピーできるボタン |
| **アクセシビリティ** | `aria-live="polite"` で新メッセージをスクリーンリーダーに通知。入力欄に `aria-label` |

### パターン7: マルチセッション管理

```
SessionStore {
  sessions:      Session[]
  activeSession: sessionId
}

Session {
  id:        string
  title:     string       // 最初のユーザーメッセージから自動生成
  messages:  Message[]
  createdAt: timestamp
  updatedAt: timestamp
}
```

- セッション切り替え時にクライアント側のチャット状態をリセットし、選択セッションの `messages` で初期化する
- 永続化先は用途に応じて選択: localStorage（プロトタイプ）、IndexedDB（オフライン対応）、サーバーDB（マルチデバイス同期）
- セッションタイトルは最初のユーザーメッセージ先頭 N 文字から自動生成。LLM にタイトル生成させると高品質だがコストと遅延が増える

### パターン9: ファイル添付・マルチモーダル入力

チャットにファイル（画像、PDF、音声等）を添付して LLM に送る機能。近年のマルチモーダルモデル普及で標準的な要件になっている。

**クライアント側のデータフロー**:

```
ユーザーがファイル選択
    │
    ▼
File → Data URL (base64) or アップロード → URL
    │
    ▼
Message.parts に file Part として格納
    │
    ▼
テキスト Part と一緒に送信
```

**ファイル送信方式の選択**:

| 方式 | 仕組み | 最大サイズ目安 | 推奨場面 |
|------|--------|---------------|----------|
| Data URL (base64 inline) | FileReader で base64 化し JSON body に含める | ~5-10 MB | 小さい画像、シンプルな実装 |
| プリアップロード + URL参照 | 先に S3 等にアップロードし URL を送信 | 無制限 | 大きいファイル、動画、本番環境 |
| マルチパート form | multipart/form-data でファイルとテキストを同時送信 | サーバー設定次第 | 従来の REST API 設計 |

**Data URL 方式の注意点**: base64 は元ファイルの約 1.33 倍のサイズになる。大きいファイルでは JSON body が肥大化し、メモリ・帯域を圧迫する。**10MB 以下の画像・PDF にはData URL、それ以上はプリアップロード方式を推奨**。

**サポートすべきファイル種別とUI表示**:

| ファイル種別 | `mediaType` パターン | メッセージ内の表示 |
|-------------|---------------------|------------------|
| 画像 | `image/*` | インライン `<img>` / サムネイル |
| PDF | `application/pdf` | `<iframe>` 埋め込み or リンク |
| 音声 | `audio/*` | `<audio>` プレイヤー |
| テキスト/CSV | `text/*` | コードブロック or プレビュー |
| その他 | - | ファイル名 + アイコン + ダウンロードリンク |

**Part モデルの拡張**:

```
FilePart extends Part {
  type:      "file"
  mediaType: string       // MIME type (例: "image/png", "application/pdf")
  url:       string       // Data URL or HTTPS URL
  filename?: string       // 元のファイル名（表示・ダウンロード用）
}
```

**UI 設計原則**:

| 原則 | 理由 |
|------|------|
| **添付プレビュー** | 送信前にサムネイル/ファイル名を表示し、削除もできるように。誤添付防止 |
| **accept 属性で制限** | `<input accept="image/*,application/pdf">` でモデルがサポートする形式のみ受付 |
| **複数ファイル対応** | `multiple` 属性。ただし合計サイズ上限を設けてUXを守る |
| **ドラッグ&ドロップ** | 入力エリアへのドロップでファイル添付。クリップボードペーストも対応するとなお良い |
| **アップロード進捗** | 大きいファイルの場合、プログレスバーを表示 |
| **送信後のクリア** | 送信完了後にファイル選択状態をリセット（`input.value = ''`） |

**サーバー側の考慮点**:

- `convertToModelMessages` 等の変換レイヤーで file Part を LLM プロバイダーが受け付ける形式に変換する
- LLM プロバイダーによってサポートする mediaType が異なる（例: GPT-4o は画像対応だがテキストファイルは非対応）。サーバーでバリデーションする
- Data URL をサーバーで受け取る場合、body サイズ制限（デフォルト 1MB 等）を引き上げる設定が必要
- ファイルの内容を信頼しない。アンチウイルススキャンやサイズ制限を適用する

### パターン8: サーバーサイド設計原則

| 原則 | 理由 |
|------|------|
| **メッセージ変換レイヤー** | UI形式とLLM形式のメッセージは構造が異なる。サーバーで変換して疎結合に |
| **system プロンプト注入** | クライアントから system を送らせない。サーバーで固定注入してプロンプトインジェクションを防ぐ |
| **認証ミドルウェア** | チャット API エンドポイントは認証必須。直接 curl されても安全に |
| **レート制限** | ユーザー単位 / IP 単位でリクエスト数を制限 |
| **タイムアウト設定** | LLM 応答は遅い。プラットフォームデフォルトのタイムアウトを超えやすいので明示的に延長 |
| **ストリームプロトコル** | SSE では `data:` 行でトークンを送り、`data: [DONE]` で完了を示すのが慣例 |

---

## Vercel AI SDK 実装ガイド（TypeScript）

以降は上記の抽象パターンを Vercel AI SDK (`useChat`) で具体実装するセクション。

## アーキテクチャ概観

```
┌─────────────────────────────────┐
│  Client (React/Vue/Svelte)      │
│  ┌───────────┐  ┌────────────┐  │
│  │ useChat   │──│ Chat UI    │  │
│  │ hook      │  │ Components │  │
│  └─────┬─────┘  └────────────┘  │
│        │ POST /api/chat          │
├────────┼────────────────────────┤
│  Server (API Route)             │
│  ┌─────▼─────┐                  │
│  │ streamText │─── LLM Provider │
│  └───────────┘                  │
└─────────────────────────────────┘
```

**データフロー**: Client が `UIMessage[]` を POST → Server が `convertToModelMessages` で変換 → `streamText` でストリーム生成 → `toUIMessageStreamResponse()` でクライアントに返却 → `useChat` がリアルタイムで UI を更新

## Phase 1: バックエンド API Route

### Next.js App Router

```typescript
// app/api/chat/route.ts
import { convertToModelMessages, streamText, UIMessage } from 'ai';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: 'openai/gpt-4o',
    system: 'You are a helpful assistant.',
    messages: await convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

### Express / 汎用 Node.js

```typescript
import { convertToModelMessages, streamText, UIMessage } from 'ai';

app.post('/api/chat', async (req, res) => {
  const { messages }: { messages: UIMessage[] } = req.body;

  const result = streamText({
    model: 'openai/gpt-4o',
    system: 'You are a helpful assistant.',
    messages: await convertToModelMessages(messages),
  });

  result.pipeUIMessageStreamToResponse(res);
});
```

### 設計判断

| 項目 | streamText | generateText |
|------|-----------|--------------|
| レスポンス | ストリーミング（SSE） | 一括返却（JSON） |
| UX | トークンが逐次表示、体感速度が良い | 全文完成まで待機 |
| 推奨場面 | チャット UI（ほぼ常にこちら） | バッチ処理、短い応答 |

`streamText` + `toUIMessageStreamResponse()` を原則使う。`generateText` は応答が極端に短い場合やバックグラウンド処理にのみ使用。

### Server 側チェックリスト

- [ ] `maxDuration` を設定（Vercel デフォルト 10s は短い）
- [ ] `system` プロンプトでアプリ固有の振る舞いを定義
- [ ] 認証・認可をミドルウェアで実施（API Route を直接叩かれても安全に）
- [ ] レート制限を検討
- [ ] エラー時に適切な HTTP ステータスを返す

## Phase 2: useChat フック設計

### 基本パターン（React）

```typescript
'use client';

import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import { useState } from 'react';

export default function ChatPage() {
  const {
    messages,
    sendMessage,
    status,
    stop,
    error,
    regenerate,
    setMessages,
  } = useChat({
    transport: new DefaultChatTransport({ api: '/api/chat' }),
  });
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage({ text: input });
    setInput('');
  };

  return (
    <div>
      <MessageList messages={messages} />
      {status === 'streaming' && (
        <button onClick={() => stop()}>Stop</button>
      )}
      {error && (
        <div>
          <p>Error occurred</p>
          <button onClick={() => regenerate()}>Retry</button>
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={status !== 'ready'}
        />
        <button type="submit" disabled={status !== 'ready'}>
          Send
        </button>
      </form>
    </div>
  );
}
```

### Vue（@ai-sdk/vue）

```typescript
import { useChat } from '@ai-sdk/vue';

const { messages, sendMessage, status, stop, error } = useChat({
  api: '/api/chat',
});
```

### Svelte（@ai-sdk/svelte）

```typescript
import { useChat } from '@ai-sdk/svelte';

const { messages, sendMessage, status, stop, error } = useChat({
  api: '/api/chat',
});
```

### useChat の主要オプションとコールバック

| オプション | 用途 |
|-----------|------|
| `transport` | カスタムトランスポート（`DefaultChatTransport` でエンドポイント指定） |
| `initialMessages` | 初期メッセージ配列（履歴復元に使用） |
| `onFinish` | アシスタント応答完了時。`{ message, messages, isAbort, isDisconnect, isError }` を受け取る |
| `onError` | エラー発生時のハンドラ |
| `onData` | データパート受信時。throw でストリーム中断可能 |

### status の状態遷移

```
ready → submitted → streaming → ready
                                  ↗
              (error) ──────────→ ready (error set)
```

- `ready`: 送信可能
- `submitted`: リクエスト送信済み、まだレスポンスなし
- `streaming`: トークン受信中
- `error` は `status` とは別の値として保持される

### 高度なパターン

**メッセージ永続化**: `onFinish` で DB に保存し、`initialMessages` で復元

```typescript
const { messages, sendMessage } = useChat({
  initialMessages: savedMessages,
  onFinish: ({ messages }) => {
    saveToDatabase(messages);
  },
});
```

**マルチチャット**: `chatId` で複数チャットセッションを分離

```typescript
const { messages, sendMessage } = useChat({
  chatId: currentChatId,
  transport: new DefaultChatTransport({
    api: `/api/chat?chatId=${currentChatId}`,
  }),
});
```

**メタデータ受信**: `onFinish` でトークン使用量等を取得

```typescript
const { messages } = useChat<MyUIMessage>({
  onFinish: ({ message }) => {
    console.log(message.metadata?.totalUsage);
  },
});
```

### ファイル添付・マルチモーダル入力

AI SDK では `sendMessage` にファイルを渡す方法が2つある。

**方法1: FileList を直接渡す（簡易）**

`<input type="file">` の FileList をそのまま `sendMessage` に渡す。SDK が自動で Data URL に変換する。

```typescript
'use client';

import { useChat } from '@ai-sdk/react';
import { useRef, useState } from 'react';

export default function ChatWithFiles() {
  const { messages, sendMessage, status } = useChat();
  const [input, setInput] = useState('');
  const [files, setFiles] = useState<FileList | undefined>(undefined);
  const fileInputRef = useRef<HTMLInputElement>(null);

  return (
    <div>
      <MessageList messages={messages} />

      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (!input.trim() && !files?.length) return;
          sendMessage({ text: input, files });
          setInput('');
          setFiles(undefined);
          if (fileInputRef.current) fileInputRef.current.value = '';
        }}
      >
        <input
          type="file"
          accept="image/*,application/pdf"
          multiple
          ref={fileInputRef}
          onChange={(e) => setFiles(e.target.files ?? undefined)}
        />
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message or attach files..."
          disabled={status !== 'ready'}
        />
        <button type="submit" disabled={status !== 'ready'}>
          Send
        </button>
      </form>
    </div>
  );
}
```

**方法2: parts 配列で明示的に構築（高度な制御）**

ファイルを手動で Data URL に変換し、`parts` 配列にテキストとファイルを混在させる。プリアップロード済み URL や画像 URL を送る場合にもこの方法を使う。

```typescript
// ファイルを Data URL に変換するユーティリティ
async function convertFilesToDataURLs(files: FileList) {
  return Promise.all(
    Array.from(files).map(
      (file) =>
        new Promise<{
          type: 'file';
          filename: string;
          mediaType: string;
          url: string;
        }>((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () =>
            resolve({
              type: 'file',
              filename: file.name,
              mediaType: file.type,
              url: reader.result as string,
            });
          reader.onerror = reject;
          reader.readAsDataURL(file);
        }),
    ),
  );
}

// 送信時
const fileParts =
  files && files.length > 0 ? await convertFilesToDataURLs(files) : [];

sendMessage({
  role: 'user',
  parts: [{ type: 'text', text: input }, ...fileParts],
});
```

**URL 参照でファイルを送る場合（プリアップロード済み / 外部画像）**:

```typescript
import { FileUIPart } from 'ai';

sendMessage({
  role: 'user',
  parts: [
    {
      type: 'file',
      mediaType: 'image/png',
      url: 'https://example.com/uploaded-image.png',
    },
    { type: 'text', text: 'この画像について説明して' },
  ],
});
```

**添付プレビューUI**:

送信前に選択されたファイルのサムネイルを表示し、個別に削除できるようにする:

```typescript
function AttachmentPreview({
  files,
  onRemove,
}: {
  files: File[];
  onRemove: (index: number) => void;
}) {
  return (
    <div className="flex gap-2 p-2">
      {files.map((file, i) => (
        <div key={i} className="relative">
          {file.type.startsWith('image/') ? (
            <img
              src={URL.createObjectURL(file)}
              alt={file.name}
              className="h-16 w-16 rounded object-cover"
            />
          ) : (
            <div className="flex h-16 w-16 items-center justify-center rounded bg-gray-100 text-xs">
              {file.name.split('.').pop()?.toUpperCase()}
            </div>
          )}
          <button
            onClick={() => onRemove(i)}
            className="absolute -right-1 -top-1 rounded-full bg-red-500 p-0.5 text-xs text-white"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
}
```

## Phase 3: UI コンポーネント設計

### メッセージリスト

```typescript
function MessageList({ messages }: { messages: UIMessage[] }) {
  return (
    <div className="flex flex-col gap-4 overflow-y-auto p-4">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
    </div>
  );
}
```

### メッセージバブル

```typescript
function MessageBubble({ message }: { message: UIMessage }) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-2 ${
          isUser
            ? 'bg-blue-500 text-white'
            : 'bg-gray-100 text-gray-900'
        }`}
      >
        {message.parts.map((part, i) => {
          switch (part.type) {
            case 'text':
              return <p key={i}>{part.text}</p>;
            case 'file':
              if (part.mediaType?.startsWith('image/')) {
                return (
                  <img
                    key={i}
                    src={part.url}
                    alt={part.filename ?? 'image'}
                    className="max-w-full rounded"
                  />
                );
              }
              if (part.mediaType === 'application/pdf') {
                return (
                  <iframe
                    key={i}
                    src={part.url}
                    title={part.filename ?? 'pdf'}
                    className="h-96 w-full rounded"
                  />
                );
              }
              return (
                <a key={i} href={part.url} download={part.filename}>
                  📎 {part.filename ?? 'file'}
                </a>
              );
            default:
              return null;
          }
        })}
      </div>
    </div>
  );
}
```

### ストリーミングインジケーター

ストリーミング中は最後のアシスタントメッセージが逐次更新される。`useChat` が自動で `messages` を更新するため、特別な処理は不要。typing インジケーターが必要な場合は `status` を使う:

```typescript
{status === 'submitted' && (
  <div className="flex gap-1 p-4">
    <span className="animate-bounce">.</span>
    <span className="animate-bounce delay-100">.</span>
    <span className="animate-bounce delay-200">.</span>
  </div>
)}
```

### 入力コンポーネント

```typescript
function ChatInput({
  value,
  onChange,
  onSubmit,
  disabled,
}: {
  value: string;
  onChange: (v: string) => void;
  onSubmit: () => void;
  disabled: boolean;
}) {
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit();
      }}
      className="flex gap-2 border-t p-4"
    >
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            onSubmit();
          }
        }}
        placeholder="Type a message..."
        disabled={disabled}
        rows={1}
        className="flex-1 resize-none rounded-lg border p-2"
      />
      <button
        type="submit"
        disabled={disabled || !value.trim()}
        className="rounded-lg bg-blue-500 px-4 py-2 text-white disabled:opacity-50"
      >
        Send
      </button>
    </form>
  );
}
```

**Enter で送信、Shift+Enter で改行** は textarea チャットUIの標準UX。

### Markdown レンダリング

アシスタントの応答に Markdown を含む場合、`react-markdown` や `marked` でレンダリングする:

```typescript
import ReactMarkdown from 'react-markdown';

{part.type === 'text' && (
  <ReactMarkdown>{part.text}</ReactMarkdown>
)}
```

### 自動スクロール

新しいメッセージ到着時に自動で最下部にスクロール:

```typescript
const scrollRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
}, [messages]);

// MessageList の末尾に <div ref={scrollRef} /> を配置
```

## Phase 4: エラーハンドリング

### クライアント側

```typescript
const { error, regenerate } = useChat({
  onError: (err) => {
    toast.error('Failed to get response. Please try again.');
  },
});
```

`error` が non-null の場合、UI にリトライボタンを表示し `regenerate()` で再試行。

### サーバー側

API Route でキャッチして適切なステータスコードを返す。`useChat` はレスポンスの HTTP ステータスを見て `error` をセットする。

## Phase 5: 既存チャットUI レビューチェックリスト

- [ ] `status` に基づいた入力の無効化（二重送信防止）
- [ ] ストリーミング中の stop ボタン
- [ ] エラー時の regenerate ボタン
- [ ] 自動スクロール（新メッセージ + ストリーミング中）
- [ ] Enter/Shift+Enter のキーバインド
- [ ] モバイル対応（仮想キーボードで入力欄が隠れない）
- [ ] Markdown レンダリング（必要なら）
- [ ] メッセージ永続化（リロードで消えない）
- [ ] アクセシビリティ（aria-live で新メッセージを通知）
- [ ] ローディング状態の視覚的フィードバック
- [ ] ファイル添付（必要なら）: accept 制限、プレビュー、送信後クリア、サイズ上限
- [ ] メッセージ内の file Part レンダリング（画像 `<img>`、PDF `<iframe>`、その他リンク）
- [ ] ドラッグ&ドロップ / クリップボードペースト対応（必要なら）

## パッケージインストール

```bash
# React
npm install ai @ai-sdk/react

# Vue
npm install ai @ai-sdk/vue

# Svelte
npm install ai @ai-sdk/svelte

# プロバイダー（例: OpenAI）
npm install @ai-sdk/openai
```

## よくある落とし穴

| 問題 | 原因 | 対処 |
|------|------|------|
| ストリームが途中で切れる | Vercel の `maxDuration` デフォルト10s | `export const maxDuration = 30;` を設定 |
| `useChat` が `'use client'` なしでエラー | Server Component で使用 | `'use client'` を先頭に追加 |
| メッセージが二重に表示される | `sendMessage` を form の onSubmit 外で呼んでいる | form の onSubmit 内で1回だけ呼ぶ |
| CORS エラー | API Route が別オリジン | 同一オリジンに配置するか CORS 設定 |
| 型エラー: `UIMessage` | AI SDK v4/v5 の破壊的変更 | `ai` パッケージのバージョンを確認 |
| ファイル送信で 413 エラー | Data URL が body サイズ制限超過 | サーバーの body サイズ上限を引き上げ（Next.js: `bodyParser: { sizeLimit: '10mb' }`） or プリアップロード方式に切り替え |
| 画像がメッセージに表示されない | `message.parts` の `type === 'file'` を処理していない | MessageBubble で `case 'file'` を追加 |
| `sendMessage` にファイルを渡してもサーバーに届かない | `convertToModelMessages` が file Part を変換済み | サーバー側のログで messages 構造を確認 |
