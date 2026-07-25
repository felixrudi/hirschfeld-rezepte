<script>
  import { onDestroy } from 'svelte';

  export let recipe;
  export let onClose;

  let currentStep = 0;
  let scaleValue = recipe.baseIngredientQty;
  let scaleRatio = 1.0;

  $: scaleRatio = scaleValue / (recipe.baseIngredientQty || 1);

  // Timer State
  let timerSeconds = 0;
  let timerRunning = false;
  let timerInterval = null;
  let timerDone = false;

  // Checkbox State for Step 0
  let checkedItems = {};

  $: totalSteps = recipe.steps?.length || 0;
  $: allChecked =
    currentStep === 0 &&
    (recipe.checklist || []).length > 0 &&
    (recipe.checklist || []).every((_, i) => checkedItems[i]);

  function handleScaleChange(e) {
    scaleValue = Number(e.target.value);
  }

  function changeStep(delta) {
    const maxSteps = totalSteps;
    if (currentStep + delta >= 0 && currentStep + delta <= maxSteps) {
      currentStep += delta;
      applyStepTimer();
    } else if (currentStep + delta > maxSteps) {
      onClose();
    }
  }

  function goToStep(i) {
    if (i >= 0 && i <= totalSteps) {
      currentStep = i;
      applyStepTimer();
    }
  }

  function toggleTimer() {
    if (timerRunning) {
      clearInterval(timerInterval);
      timerRunning = false;
      return;
    }
    // Restart from step duration when finished or empty
    if (timerSeconds <= 0 || timerDone) {
      const stepTimer = currentStep > 0 ? recipe.steps[currentStep - 1]?.timer : 0;
      if (!stepTimer) return;
      timerSeconds = stepTimer;
      timerDone = false;
    }
    timerRunning = true;
    timerInterval = setInterval(() => {
      if (timerSeconds > 0) {
        timerSeconds--;
      } else {
        clearInterval(timerInterval);
        timerRunning = false;
        timerDone = true;
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
          navigator.vibrate([200, 100, 200]);
        }
      }
    }, 1000);
  }

  function applyStepTimer() {
    clearInterval(timerInterval);
    timerRunning = false;
    timerDone = false;
    if (currentStep > 0 && recipe.steps[currentStep - 1]?.timer) {
      timerSeconds = recipe.steps[currentStep - 1].timer;
    } else {
      timerSeconds = 0;
    }
  }

  // Initial timer when opening a cooking step
  $: if (currentStep > 0) {
    // reactive guard: only reset when step changes via applyStepTimer in changeStep
  }

  onDestroy(() => {
    clearInterval(timerInterval);
  });

  function formatTime(secs) {
    const h = Math.floor(secs / 3600);
    const m = Math.floor((secs % 3600) / 60);
    const s = secs % 60;
    if (h > 0) {
      return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }

  function formatTimerLabel(secs) {
    if (!secs) return '';
    if (secs >= 3600) {
      const h = Math.round(secs / 3600);
      return `~${h} Std`;
    }
    const m = Math.round(secs / 60);
    return m >= 1 ? `${m} Min` : `${secs} Sek`;
  }

  function parallelText(raw) {
    if (!raw) return '';
    return raw
      .replace(/^⚡\s*/g, '')
      .replace(/PARALLEL JETZT ERLEDIGEN:\s*/gi, '')
      .replace(/PARALLEL ERLEDIGEN:\s*/gi, '')
      .replace(/Parallel möglich:\s*/gi, '')
      .replace(/Parallel:\s*/gi, '')
      .trim();
  }

  function bodyIsRedundant(step) {
    if (!step?.body) return true;
    return step.body.trim() === step.header.trim();
  }
</script>

<div class="kitchen-modal" role="dialog" aria-modal="true" aria-label="Kochmodus {recipe.title}">
  <div class="stepper-screen">
    <!-- Top bar -->
    <header class="screen-top">
      <div class="top-left">
        <div class="recipe-name">{recipe.title}</div>
        <div class="step-meta">
          {#if currentStep === 0}
            Vorbereitung · Zutaten abhaken
          {:else}
            Schritt {currentStep} / {totalSteps}
            {#if recipe.steps[currentStep - 1]?.timer}
              · ⏱ {formatTimerLabel(recipe.steps[currentStep - 1].timer)}
            {/if}
          {/if}
        </div>
      </div>
      <button class="close-btn" on:click={onClose} aria-label="Schließen">✕</button>
    </header>

    <!-- Progress -->
    <div class="progress" aria-hidden="true">
      {#each Array(totalSteps + 1) as _, i}
        <button
          class="seg {i === currentStep ? 'active' : ''} {i < currentStep ? 'done' : ''}"
          on:click={() => goToStep(i)}
          title={i === 0 ? 'Zutaten' : recipe.steps[i - 1]?.header}
        ></button>
      {/each}
    </div>

    <!-- Main content: one full screen card -->
    <div class="screen-body">
      {#if currentStep === 0}
        <div class="scaler-box">
          <div class="scaler-header">
            <span class="scaler-title">⚖️ Menge skalieren</span>
            <span class="scaler-val">
              {recipe.baseIngredientName}: {scaleValue}{recipe.unit}
              ({Math.round(scaleRatio * 100)}%)
            </span>
          </div>
          <input
            type="range"
            class="scaler-slider"
            min={Math.max(1, Math.round((recipe.baseIngredientQty || 1) * 0.3))}
            max={Math.round((recipe.baseIngredientQty || 1) * 1.5)}
            step={recipe.unit === 'g' || recipe.unit === 'ml' ? 10 : 1}
            value={scaleValue}
            on:input={handleScaleChange}
          />
          <p class="scaler-hint">Regler auf deinen Vorrat — Zutaten passen sich live an.</p>
        </div>

        <div class="step-stage prep">
          <div class="stage-kicker">MISE EN PLACE</div>
          <h1 class="stage-title">Zutaten bereitlegen</h1>
          <p class="stage-lead">Alles abhaken, dann loskochen. Ein Haken = greifbar auf der Arbeitsfläche.</p>

          <div class="check-grid">
            {#each recipe.checklist || [] as item, idx}
              {@const scaledQty = Math.round(item.baseQty * scaleRatio * 10) / 10}
              <label class="check-item {checkedItems[idx] ? 'checked' : ''}">
                <input type="checkbox" bind:checked={checkedItems[idx]} />
                <span class="check-text">
                  <strong class="qty">{scaledQty} {item.unit}</strong>
                  <span class="iname">{item.name}</span>
                </span>
              </label>
            {/each}
          </div>
        </div>
      {:else}
        {@const step = recipe.steps[currentStep - 1]}
        <div class="step-stage cook">
          <div class="stage-kicker">
            SCHRITT {currentStep} VON {totalSteps}
            {#if step.timer}
              <span class="kicker-time">⏱ {formatTimerLabel(step.timer)}</span>
            {/if}
          </div>
          <h1 class="stage-title">{step.header}</h1>

          {#if !bodyIsRedundant(step)}
            <p class="stage-body">{step.body}</p>
          {/if}

          {#if step.parallel}
            <div class="parallel-box">
              <div class="parallel-badge">⚡ PARALLEL</div>
              <div class="parallel-text">{parallelText(step.parallel)}</div>
            </div>
          {/if}

          {#if step.timer}
            <div class="timer-panel {timerDone ? 'done' : ''} {timerRunning ? 'running' : ''}">
              <div class="timer-left">
                <div class="timer-label">{timerDone ? '⏰ Fertig!' : 'Schritt-Timer'}</div>
                <div class="timer-clock">{formatTime(timerSeconds)}</div>
              </div>
              <button class="btn-timer" on:click={toggleTimer}>
                {#if timerDone}
                  Nochmal
                {:else if timerRunning}
                  Pausieren ⏸
                {:else}
                  Start ▶
                {/if}
              </button>
            </div>
          {/if}
        </div>
      {/if}
    </div>

    <!-- Bottom nav: big, thumb-friendly -->
    <footer class="screen-nav">
      <button class="btn-nav btn-prev" disabled={currentStep === 0} on:click={() => changeStep(-1)}>
        ⇠ Zurück
      </button>
      <button class="btn-nav btn-next" on:click={() => changeStep(1)}>
        {#if currentStep === 0}
          {allChecked ? 'Alles da — Loskochen ➔' : 'Loskochen ➔'}
        {:else if currentStep === totalSteps}
          🎉 Fertig · Guten Appetit
        {:else}
          Nächster Schritt ➔
        {/if}
      </button>
    </footer>
  </div>
</div>

<style>
  .kitchen-modal {
    position: fixed;
    inset: 0;
    background: #0c0a09;
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: stretch;
  }

  .stepper-screen {
    width: 100%;
    max-width: 720px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    min-height: 100%;
    min-height: 100dvh;
    background: var(--bg-card, #241f1c);
    border-left: 1px solid var(--border-color, #3d342d);
    border-right: 1px solid var(--border-color, #3d342d);
  }

  .screen-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 16px 20px 10px;
    border-bottom: 1px solid var(--border-color, #3d342d);
    flex-shrink: 0;
  }

  .recipe-name {
    font-size: 15px;
    font-weight: 700;
    color: var(--accent-gold, #e5a43b);
    letter-spacing: 0.02em;
  }

  .step-meta {
    font-size: 12px;
    color: var(--text-muted, #a6988d);
    margin-top: 2px;
  }

  .close-btn {
    background: #191513;
    border: 1px solid var(--border-color, #3d342d);
    color: var(--text-muted, #a6988d);
    width: 40px;
    height: 40px;
    border-radius: 12px;
    font-size: 18px;
    cursor: pointer;
    flex-shrink: 0;
  }

  .progress {
    display: flex;
    gap: 4px;
    padding: 12px 20px 0;
    flex-shrink: 0;
  }

  .seg {
    flex: 1;
    height: 5px;
    background: #191513;
    border: none;
    border-radius: 3px;
    padding: 0;
    cursor: pointer;
    transition: background 0.2s;
  }
  .seg.active { background: var(--accent-gold, #e5a43b); }
  .seg.done { background: var(--accent-green, #4caf50); }

  .screen-body {
    flex: 1;
    overflow-y: auto;
    padding: 16px 20px 12px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .scaler-box {
    background: #191513;
    border: 1px solid var(--accent-gold, #e5a43b);
    border-radius: 14px;
    padding: 14px 16px;
    flex-shrink: 0;
  }

  .scaler-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
    flex-wrap: wrap;
  }

  .scaler-title {
    font-size: 12px;
    font-weight: 700;
    color: var(--accent-gold, #e5a43b);
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  .scaler-val {
    font-size: 13px;
    font-family: var(--font-mono, monospace);
    font-weight: 700;
  }

  .scaler-slider {
    width: 100%;
    accent-color: var(--accent-gold, #e5a43b);
    cursor: pointer;
  }

  .scaler-hint {
    font-size: 11px;
    color: var(--text-muted, #a6988d);
    margin-top: 6px;
  }

  /* One step = one stage, large type */
  .step-stage {
    background: #191513;
    border: 1px solid var(--border-color, #3d342d);
    border-radius: 18px;
    padding: 24px 22px;
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: min(62vh, 520px);
  }

  .stage-kicker {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-gold, #e5a43b);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }

  .kicker-time {
    background: rgba(229, 164, 59, 0.15);
    border: 1px solid rgba(229, 164, 59, 0.35);
    padding: 2px 10px;
    border-radius: 999px;
    letter-spacing: 0.02em;
    font-size: 11px;
  }

  .stage-title {
    font-size: clamp(22px, 5vw, 30px);
    font-weight: 800;
    line-height: 1.25;
    color: var(--text-main, #f5ede6);
    margin-bottom: 16px;
  }

  .stage-lead {
    font-size: 14px;
    color: var(--text-muted, #a6988d);
    margin-bottom: 16px;
    line-height: 1.5;
  }

  .stage-body {
    font-size: clamp(17px, 3.6vw, 20px);
    line-height: 1.55;
    color: var(--text-main, #f5ede6);
    white-space: pre-wrap;
    margin-bottom: 20px;
    flex: 1;
  }

  .check-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 8px;
    margin-top: 4px;
  }

  @media (min-width: 520px) {
    .check-grid {
      grid-template-columns: 1fr 1fr;
    }
  }

  .check-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: #241f1c;
    border: 1px solid var(--border-color, #3d342d);
    padding: 12px 14px;
    border-radius: 12px;
    cursor: pointer;
    user-select: none;
    transition: all 0.15s;
  }

  .check-item:hover { border-color: var(--accent-gold, #e5a43b); }
  .check-item.checked {
    background: rgba(76, 175, 80, 0.1);
    border-color: var(--accent-green, #4caf50);
    opacity: 0.75;
  }
  .check-item.checked .check-text { text-decoration: line-through; }
  .check-item input[type="checkbox"] {
    width: 20px;
    height: 20px;
    margin-top: 2px;
    accent-color: var(--accent-gold, #e5a43b);
    flex-shrink: 0;
  }

  .check-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
    font-size: 14px;
  }

  .qty {
    font-family: var(--font-mono, monospace);
    font-size: 13px;
    color: var(--accent-gold, #e5a43b);
  }

  .iname {
    color: var(--text-main, #f5ede6);
    line-height: 1.35;
  }

  .parallel-box {
    background: rgba(229, 164, 59, 0.1);
    border: 1.5px solid var(--accent-gold, #e5a43b);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 16px;
  }

  .parallel-badge {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.1em;
    color: var(--accent-gold, #e5a43b);
    margin-bottom: 6px;
  }

  .parallel-text {
    font-size: 15px;
    font-weight: 500;
    line-height: 1.45;
    color: var(--text-main, #f5ede6);
    white-space: pre-wrap;
  }

  .timer-panel {
    margin-top: auto;
    background: #120e0d;
    border: 1px solid var(--border-color, #3d342d);
    border-radius: 14px;
    padding: 16px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
  }

  .timer-panel.running {
    border-color: var(--accent-gold, #e5a43b);
  }

  .timer-panel.done {
    border-color: var(--accent-green, #4caf50);
    background: rgba(76, 175, 80, 0.12);
  }

  .timer-label {
    font-size: 11px;
    color: var(--text-muted, #a6988d);
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .timer-clock {
    font-family: var(--font-mono, monospace);
    font-size: 36px;
    font-weight: 700;
    color: var(--accent-gold, #e5a43b);
    line-height: 1.1;
  }

  .timer-panel.done .timer-clock {
    color: var(--accent-green, #4caf50);
  }

  .btn-timer {
    background: var(--accent-gold, #e5a43b);
    color: #161210;
    border: none;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    white-space: nowrap;
  }

  .screen-nav {
    display: flex;
    gap: 10px;
    padding: 12px 20px calc(16px + env(safe-area-inset-bottom, 0px));
    border-top: 1px solid var(--border-color, #3d342d);
    background: #1a1614;
    flex-shrink: 0;
  }

  .btn-nav {
    flex: 1;
    padding: 16px 12px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 700;
    border: none;
    cursor: pointer;
    transition: opacity 0.15s;
  }

  .btn-prev {
    flex: 0.45;
    background: #191513;
    border: 1px solid var(--border-color, #3d342d);
    color: var(--text-main, #f5ede6);
  }

  .btn-next {
    flex: 1;
    background: var(--accent-gold, #e5a43b);
    color: #161210;
  }

  .btn-prev:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  @media (max-width: 480px) {
    .stage-title { font-size: 22px; }
    .stage-body { font-size: 17px; }
    .timer-clock { font-size: 30px; }
    .step-stage { min-height: 50vh; padding: 20px 16px; }
  }
</style>
