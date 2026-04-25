# Brainstorm Automation Examples

Use this file to see how the brainstorming pipeline works end to end.

## Example 1: SaaS onboarding improvement

### Raw request

Improve activation in the first 7 days for our B2B SaaS onboarding. We cannot add headcount this quarter. I want practical ideas, not abstract innovation theater.

### Theme clarifier output

```yaml
clarified_theme: Improve first-7-day activation for a B2B SaaS onboarding flow without increasing team size
objective: Increase activation and reduce setup abandonment
audience: New B2B SaaS users
constraints:
  - no headcount increase this quarter
  - prefer changes that can ship quickly
  - practical ideas over abstract brand concepts
time_horizon: this quarter
success_criteria:
  - higher activation within 7 days
  - lower drop-off during setup
mode:
  setting: solo
  flow: divergence_then_synthesis
  orientation: business
open_questions:
  - which setup step has the biggest drop-off?
```

### Framework selector output

```yaml
primary_framework: SCAMPER
secondary_framework: JTBD
why:
  - there is already an onboarding flow to modify rather than invent from zero
  - ideas should later be grounded in user value rather than feature novelty
rejected_alternatives:
  - framework: Mind map
    reason: useful for solo exploration, but weaker for systematic modification of an existing flow
run_order:
  - SCAMPER
  - JTBD
notes_for_next_agent:
  - focus on setup friction, motivation, and time-to-value
```

### Divergence sample

```yaml
framework_used: SCAMPER
idea_groups:
  - group: Substitute
    ideas:
      - title: Replace manual setup with templates
        description: Offer prebuilt workspace templates for common use cases
        rationale: reduces blank-page friction
  - group: Combine
    ideas:
      - title: Combine onboarding with first-value checklist
        description: Merge setup steps with an explicit value milestone tracker
        rationale: setup feels more meaningful when tied to outcomes
  - group: Eliminate
    ideas:
      - title: Remove optional fields from initial setup
        description: Defer low-value configuration until after first success
        rationale: cuts early abandonment risk
observations:
  - many strong ideas reduce setup friction rather than add education
```

### Clustering sample

```yaml
clusters:
  - name: Reduce setup friction
    theme: Make the first session easier to complete
    representative_ideas:
      - title: Replace manual setup with templates
        description: Start users from ready-made setups
      - title: Remove optional fields from initial setup
        description: Push non-critical configuration later
    included_idea_refs:
      - Substitute.Replace manual setup with templates
      - Eliminate.Remove optional fields from initial setup
  - name: Increase time-to-value visibility
    theme: Show progress and outcome early
    representative_ideas:
      - title: Combine onboarding with first-value checklist
        description: Tie setup to visible progress milestones
    included_idea_refs:
      - Combine.Combine onboarding with first-value checklist
discarded_duplicates: []
outliers_to_keep:
  - title: concierge kickoff video
    reason: higher effort but may be useful for high-value accounts
synthesis_notes:
  - the strongest pattern is reducing effort before adding motivation layers
```

### Business framing sample

```yaml
framework_used: JTBD
jobs_to_be_done:
  - job: Help me get to initial value without having to understand the whole product
    supporting_clusters:
      - Reduce setup friction
      - Increase time-to-value visibility
errc:
  eliminate:
    - unnecessary setup fields
  reduce:
    - cognitive load in first session
  raise:
    - clarity of next best step
  create:
    - a visible first-value milestone
business_implications:
  - activation improvements likely come more from simplicity than education content
key_assumptions:
  - the main bottleneck is setup friction, not lead quality
```

### Ranking sample

```yaml
top_candidates:
  - idea: template-based onboarding with deferred advanced setup
    from_cluster: Reduce setup friction
    score:
      impact: 5
      speed: 4
      implementation_cost: 3
      strategic_fit: 5
      novelty: 2
      confidence: 4
    why:
      - directly attacks setup friction
      - can likely ship without major org change
    key_assumptions:
      - templates match common customer starting points
  - idea: first-value checklist with progress visibility
    from_cluster: Increase time-to-value visibility
    score:
      impact: 4
      speed: 4
      implementation_cost: 2
      strategic_fit: 5
      novelty: 2
      confidence: 4
    why:
      - gives users a clear sense of forward motion
    key_assumptions:
      - visible progress changes completion behavior
watchouts:
  - adding more UI without removing friction could backfire
```

### Experiment plan sample

```yaml
experiments:
  - idea: template-based onboarding with deferred advanced setup
    hypothesis: users activate faster if the first session starts from a near-ready state
    test: expose templates to 50% of new signups for 2 weeks
    success_metric: activation within 7 days
    leading_indicator: setup completion rate in first session
    failure_signal: no activation lift and increased template confusion
    effort_level: medium
    next_decision: revise
  - idea: first-value checklist with progress visibility
    hypothesis: users complete setup more often when they can see the path to first value
    test: add a 3-step first-value checklist for one onboarding segment
    success_metric: checklist completion and activation rate
    leading_indicator: step-1 completion rate
    failure_signal: users ignore checklist and time-on-task worsens
    effort_level: low
    next_decision: ship
notes:
  - run both tests on segments with similar acquisition quality
```

### Final user-facing answer shape

- Primary framework: SCAMPER
- Secondary framework: JTBD
- Best ideas: template onboarding, deferred advanced settings, first-value checklist
- Next actions: run 2 small experiments and measure setup completion + activation

## Example 2: New business concept generation

### Raw request

We want new product ideas for a small B2B AI company. We need ideas that can become paid pilots quickly, not moonshots.

### Suggested pipeline

- Theme Clarifier
- Framework Selector
- Divergence Agent
- Business Framing Agent
- Ranking Agent
- Experiment Designer

### Recommended frameworks

- Primary: Random stimulus
- Secondary: JTBD

Why:
- random stimulus helps escape obvious AI SaaS clichés
- JTBD keeps ideas grounded in buyer pain and pilotability

### Good output pattern

- raw surprising ideas from random connections
- translation into customer jobs
- shortlist by pilot speed, value density, and sales plausibility
- 2 to 3 pilot offers to test

## Example 3: Team workshop on pricing strategy

### Raw request

Design a workshop for our leadership team to rethink pricing. The current discussion goes in circles and the loudest person dominates.

### Suggested pipeline

- Theme Clarifier
- Framework Selector
- Facilitation-oriented Divergence Agent
- Clustering Agent
- Ranking Agent
- Final Synthesis

### Recommended frameworks

- Primary: Six Thinking Hats
- Secondary: ERRC

Why:
- Six Thinking Hats forces the room to separate facts, fears, upside, and creative options
- ERRC helps convert discussion into concrete pricing-structure moves

### Good output pattern

- session agenda
- hat-by-hat prompts
- captured pricing options
- ERRC summary
- shortlist of pricing experiments

## Example 4: Too many messy content ideas

### Raw request

We have 50 rough newsletter topic ideas and no structure. Help us organize them and find the strongest themes.

### Suggested pipeline

- Theme Clarifier
- Framework Selector
- Clustering Agent
- Ranking Agent
- Final Synthesis

### Recommended frameworks

- Primary: KJ method
- Secondary: Why / How ladder

Why:
- KJ method is best for grouping noisy idea sets
- Why / How ladder helps connect topic themes to editorial goals and execution

### Good output pattern

- clusters by audience/problem/theme
- named editorial lanes
- top recurring themes
- next 4 topics to publish

## How to read these examples

Do not copy them mechanically.

Use them to understand:
- how to choose frameworks
- how to sequence agents
- what good intermediate outputs look like
- how to turn brainstorming into action instead of just idea lists
