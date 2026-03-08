# Sources and query templates (Japan: 補助金・助成金)

Prefer primary sources. Use secondary sources only for discovery, then confirm with primary.

## Primary sources (recommended)

- J-Grants: https://www.jgrants-portal.go.jp/
- Government ministries/agencies (`*.go.jp`)
  - METI / SME Agency (中小企業庁): https://www.chusho.meti.go.jp/
  - MHLW (厚生労働省): https://www.mhlw.go.jp/
- Local government (`*.lg.jp`)
  - Prefectures, municipalities (frequently publish their own calls)

For award-result checks, prioritize official public pages on `chusho.meti.go.jp`, `meti.go.jp`, and `*.lg.jp` before J-Grants. J-Grants currently has a restrictive `robots.txt` (`Disallow: /`, `Allow: /index.html`), which can reduce automated discovery coverage.

## Public support orgs (usually reliable; still confirm)

- SMRJ (中小企業基盤整備機構): https://www.smrj.go.jp/
- J-Net21 (SME support portal): https://j-net21.smrj.go.jp/
- JETRO: https://www.jetro.go.jp/

## Executing secretariat sites (discovery only)

Many major subsidy programs are run via an executing secretariat site. These are useful for
finding the latest application portal/PDFs, but treat them as discovery and still confirm
eligibility/deadlines against the most authoritative documents.

- IT導入補助金: https://it-hojo.jp/
- 小規模事業者持続化補助金: https://www.jizokukahojokin.info/
- ものづくり補助金: https://www.monodukuri-hojo.jp/

## Past award/adoption result pages (high value for fit assessment)

When available, search official pages and PDFs for:

- `採択結果`
- `採択者一覧`
- `採択事例`
- `交付決定`
- `採択`

Use only official public pages/PDFs to understand what kinds of applicants and projects were actually selected, but do not treat them as a guarantee of future eligibility or acceptance.

## Secondary sources (discovery only)

- Chambers of commerce / SME support centers

## Search query templates

Use Japanese keywords; include official terms that appear in calls.

- General discovery:
  - `補助金 公募 令和` / `助成金 公募` / `募集要項` / `公募要領` / `交付要綱`
- Official-site constrained:
  - `site:jgrants-portal.go.jp 補助金 {topic}`
  - `site:go.jp 補助金 公募 {topic}`
  - `site:lg.jp 補助金 公募 {prefecture} {topic}`
- Past result discovery:
  - `site:go.jp {program-name} 採択結果`
  - `site:lg.jp {program-name} 採択者一覧`
  - `site:go.jp {program-name} 交付決定 pdf`
  - `site:monodukuri-hojo.jp {program-name} 採択結果`
- Purpose-oriented:
  - DX/IT: `IT導入`, `DX`, `デジタル化`
  - Hiring/wages: `キャリアアップ助成金`, `人材開発支援`, `賃上げ`
  - Energy saving: `省エネ`, `設備更新`, `脱炭素`
  - R&D: `研究開発`, `実証`, `共同研究`

## What to extract (minimum fields)

- Program name
- Administering body (ministry / prefecture / executing org)
- Target region (national / specific prefecture/city)
- Eligible applicants
- Eligible costs
- Amount / rate
- Deadline / application window
- How to apply (J-Grants / online form / postal / via support org)
- Official URL + any official PDF URLs
