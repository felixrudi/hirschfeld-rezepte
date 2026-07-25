<script>
  import { onDestroy } from 'svelte';

  export let recipe;
  export let onClose;

  let currentStep = 0;
  let scaleValue = recipe.baseIngredientQty;
  let scaleRatio = 1.0;

  $: scaleRatio = scaleValue / recipe.baseIngredientQty;

  // Timer State
  let timerSeconds = 0;
  let timerRunning = false;
  let timerInterval = null;

  // Checkbox State for Step 0
  let checkedItems = {};

  function handleScaleChange(e) {
    scaleValue = Number(e.target.value);
  }

  function changeStep(delta) {
    const maxSteps = recipe.steps.length;
    if (currentStep + delta >= 0 && currentStep + delta <= maxSteps) {
      currentStep += delta;
      resetStepTimer();
    } else if (currentStep + delta > maxSteps) {
      alert('🎉 Guten Appetit! Kochvorgang abgeschlossen.');
      onClose();
    }
  }

  function toggleTimer() {
    if (timerRunning) {
      clearInterval(timerInterval);
      timerRunning = false;
    } else {
      timerRunning = true;
      timerInterval = setInterval(() => {
        if (timerSeconds > 0) {
          timerSeconds--;
        } else {
          clearInterval(timerInterval);
          timerRunning = false;
          alert('⏰ Timer abgelaufen!');
        }
      }, 1000);
    }
  }

  function resetStepTimer() {
    clearInterval(timerInterval);
    timerRunning = false;
    if (currentStep > 0 && recipe.steps[currentStep - 1].timer) {
      timerSeconds = recipe.steps[currentStep - 1].timer;
    } else {
      timerSeconds = 0;
    }
  }

  $: if (currentStep > 0 && recipe.steps[currentStep - 1]) {
    resetStepTimer();
  }

  onDestroy(() => {
    clearInterval(timerInterval);
  });

  function formatTime(secs) {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }
</script>

<div class="kitchen-modal">
  <div class="stepper-container">
    <div class="modal-header">
      <div>
        <h2>{recipe.title}</h2>
        <p class="subtitle">
          {#if currentStep === 0}
            Schritt 0: Smart-Scaler & Zutaten-Check
          {:else}
            Schritt {currentStep} von {recipe.steps.length}: {recipe.steps[currentStep - 1].header}
          {/if}
        </p>
      </div>
      <button class="close-modal" on:click={onClose}>✕</button>
    </div>

    <!-- Segmented Progress Bar -->
    <div class="step-progress-bar">
      {#each Array(recipe.steps.length + 1) as _, i}
        <div 
          class="progress-segment {i === currentStep ? 'active' : (i < currentStep ? 'done' : '')}"
        ></div>
      {/each}
    </div>

    {#if currentStep === 0}
      <!-- SMART SCALER BOX IN STEP 0 -->
      <div class="scaler-box">
        <div class="scaler-header">
          <span class="scaler-title">⚖️ Resteverwertungs-Regler (Smart Scaler)</span>
          <span class="scaler-val">{recipe.baseIngredientName}: {scaleValue}{recipe.unit} ({Math.round(scaleRatio * 100)}% Batch)</span>
        </div>
        <input 
          type="range" 
          class="scaler-slider" 
          min={Math.round(recipe.baseIngredientQty * 0.3)} 
          max={Math.round(recipe.baseIngredientQty * 1.5)} 
          step="50" 
          value={scaleValue} 
          on:input={handleScaleChange}
        />
        <p class="scaler-hint">Ziehe den Regler auf deinen Vorrat — alle weiteren Zutaten & Makros passen sich live an!</p>
      </div>

      <!-- STEP 0 CHECKLIST -->
      <div class="step-card">
        <div class="step-number">VORBEREITUNG (MISE EN PLACE)</div>
        <div class="step-title">Zutaten & Equipment abhaken</div>
        
        <div class="check-grid">
          {#each recipe.checklist as item, idx}
            {@const scaledQty = Math.round(item.baseQty * scaleRatio * 10) / 10}
            <label class="check-item {checkedItems[idx] ? 'checked' : ''}">
              <input type="checkbox" bind:checked={checkedItems[idx]} />
              <span><strong>{scaledQty} {item.unit}</strong> {item.name}</span>
            </label>
          {/each}
        </div>
      </div>
    {:else}
      <!-- STEP 1..N COOKING -->
      {@const step = recipe.steps[currentStep - 1]}
      <div class="step-card">
        <div class="step-number">SCHRITT {currentStep} VON {recipe.steps.length}</div>
        <div class="step-title">{step.header}</div>
        <div class="step-text">{step.body}</div>

        {#if step.parallel}
          <div class="parallel-box">
            <div class="parallel-icon">⚡</div>
            <div>
              <div class="parallel-title">PARALLEL ERLEDIGEN (während Köchelzeit):</div>
              <div class="parallel-text">{step.parallel.replace('⚡ PARALLEL JETZT ERLEDIGEN: ', '').replace('⚡ PARALLEL ERLEDIGEN: ', '')}</div>
            </div>
          </div>
        {/if}

        {#if step.timer}
          <div class="step-timer-box">
            <div>
              <div class="timer-label">Schritt-Timer:</div>
              <div class="timer-clock">{formatTime(timerSeconds)}</div>
            </div>
            <button class="btn-step-timer" on:click={toggleTimer}>
              {timerRunning ? 'Timer Pausieren ⏸' : 'Timer Starten ▶'}
            </button>
          </div>
        {/if}
      </div>
    {/if}

    <div class="stepper-nav">
      <button class="btn-nav btn-prev" disabled={currentStep === 0} on:click={() => changeStep(-1)}>
        ⇠ Zurück
      </button>
      <button class="btn-nav btn-next" on:click={() => changeStep(1)}>
        {currentStep === 0 ? 'Alles bereit? Loskochen ➔' : (currentStep === recipe.steps.length ? '🎉 Fertigstellen!' : 'Nächster Schritt ➔')}
      </button>
    </div>
  </div>
</div>

<style>
  .kitchen-modal {
    position: fixed;
    inset: 0;
    background: rgba(12, 10, 9, 0.96);
    backdrop-filter: blur(10px);
    z-index: 1000;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-y: auto;
  }

  .stepper-container {
    background: var(--bg-card);
    border: 1px solid var(--accent-gold);
    border-radius: 20px;
    max-width: 740px;
    width: 100%;
    padding: 28px;
    box-shadow: 0 16px 48px rgba(0,0,0,0.7);
    position: relative;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 14px;
  }

  .modal-header h2 {
    font-size: 22px;
    font-weight: 700;
    color: var(--accent-gold);
  }

  .subtitle {
    font-size: 13px;
    color: var(--text-muted);
  }

  .close-modal {
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-size: 26px;
    cursor: pointer;
  }

  .step-progress-bar {
    display: flex;
    gap: 6px;
    margin-bottom: 20px;
  }

  .progress-segment {
    flex: 1;
    height: 6px;
    background: #191513;
    border-radius: 4px;
    transition: background 0.3s;
  }

  .progress-segment.active { background: var(--accent-gold); }
  .progress-segment.done { background: var(--accent-green); }

  .scaler-box {
    background: #191513;
    border: 1px solid var(--accent-gold);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 20px;
  }

  .scaler-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }

  .scaler-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--accent-gold);
  }

  .scaler-val {
    font-size: 13px;
    font-family: var(--font-mono);
    font-weight: 700;
  }

  .scaler-slider {
    width: 100%;
    accent-color: var(--accent-gold);
    cursor: pointer;
  }

  .scaler-hint {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 6px;
  }

  .step-card {
    background: #191513;
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
  }

  .step-number {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--accent-gold);
    margin-bottom: 6px;
  }

  .step-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
    color: var(--text-main);
  }

  .step-text {
    font-size: 15px;
    color: var(--text-main);
    line-height: 1.6;
    margin-bottom: 16px;
  }

  .check-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 12px;
  }

  .check-item {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #241f1c;
    border: 1px solid var(--border-color);
    padding: 10px 14px;
    border-radius: 10px;
    cursor: pointer;
    user-select: none;
    transition: all 0.2s;
  }

  .check-item:hover { border-color: var(--accent-gold); }
  .check-item.checked { background: rgba(76, 175, 80, 0.1); border-color: var(--accent-green); color: var(--text-muted); }
  .check-item.checked span { text-decoration: line-through; }
  .check-item input[type="checkbox"] { width: 18px; height: 18px; accent-color: var(--accent-gold); }

  .parallel-box {
    background: rgba(229, 164, 59, 0.1);
    border: 1px solid var(--accent-gold);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 16px;
    display: flex;
    gap: 12px;
    align-items: flex-start;
  }

  .parallel-icon { font-size: 22px; }
  .parallel-title { font-size: 13px; font-weight: 700; color: var(--accent-gold); text-transform: uppercase; margin-bottom: 2px; }
  .parallel-text { font-size: 14px; color: var(--text-main); font-weight: 500; }

  .step-timer-box {
    background: #120e0d;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  .timer-label { font-size: 12px; color: var(--text-muted); text-transform: uppercase; }
  .timer-clock { font-family: var(--font-mono); font-size: 28px; font-weight: 700; color: var(--accent-gold); }
  .btn-step-timer { background: var(--accent-gold); color: #161210; border: none; padding: 8px 18px; border-radius: 8px; font-size: 14px; font-weight: 700; cursor: pointer; }

  .stepper-nav { display: flex; justify-content: space-between; gap: 12px; }
  .btn-nav { flex: 1; padding: 12px; border-radius: 10px; font-size: 15px; font-weight: 700; border: none; cursor: pointer; transition: all 0.2s; }
  .btn-prev { background: #191513; border: 1px solid var(--border-color); color: var(--text-main); }
  .btn-next { background: var(--accent-gold); color: #161210; }
  .btn-prev:disabled { opacity: 0.3; cursor: not-allowed; }
</style>
