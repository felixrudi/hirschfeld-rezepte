<script>
  import { createEventDispatcher } from 'svelte';

  export let recipe = null; // null for new recipe, or existing recipe object to edit
  export let isOpen = false;

  const dispatch = createEventDispatcher();

  let title = recipe?.title || "";
  let category = recipe?.category || "Hauptmahlzeit";
  let rating = recipe?.rating || 5;
  let prepTimeMin = recipe?.prepTimeMin || 30;
  let kcalPortion = recipe?.kcalPortion || 400;
  let proteinPortion = recipe?.proteinPortion || 25;
  let batch = recipe?.batch ?? true;
  let portionen = recipe?.portionen || 4;
  let einfrierbar = recipe?.einfrierbar ?? true;
  let image = recipe?.image || "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80";

  let checklist = recipe?.checklist ? JSON.parse(JSON.stringify(recipe.checklist)) : [
    { name: "", baseQty: 500, unit: "g" }
  ];

  let steps = recipe?.steps ? JSON.parse(JSON.stringify(recipe.steps)) : [
    { header: "Vorbereitung", body: "", parallel: "", timer: null }
  ];

  function addIngredient() {
    checklist = [...checklist, { name: "", baseQty: 100, unit: "g" }];
  }

  function removeIngredient(index) {
    checklist = checklist.filter((_, i) => i !== index);
  }

  function addStep() {
    steps = [...steps, { header: `Schritt ${steps.length + 1}`, body: "", parallel: "", timer: null }];
  }

  function removeStep(index) {
    steps = steps.filter((_, i) => i !== index);
  }

  function handleSave() {
    if (!title.trim()) {
      alert("Bitte einen Titel eingeben.");
      return;
    }

    const savedRecipe = {
      id: recipe?.id || title.toLowerCase().replace(/[^a-z0-9]/g, '-'),
      title,
      category,
      rating: Number(rating),
      prepTimeMin: Number(prepTimeMin),
      kcalPortion: Number(kcalPortion),
      proteinPortion: Number(proteinPortion),
      batch,
      portionen: Number(portionen),
      einfrierbar,
      image,
      checklist: checklist.filter(i => i.name.trim() !== ""),
      steps: steps.filter(s => s.body.trim() !== "" || s.header.trim() !== "")
    };

    dispatch('save', savedRecipe);
    close();
  }

  function close() {
    dispatch('close');
  }
</script>

{#if isOpen}
<div class="modal-backdrop" on:click={close}>
  <div class="modal-card" on:click|stopPropagation>
    <div class="modal-header">
      <h2>{recipe ? '✏️ Rezept bearbeiten' : '➕ Neues Rezept anlegen'}</h2>
      <button class="btn-close" on:click={close}>✕</button>
    </div>

    <div class="modal-body">
      <div class="form-grid">
        <div class="form-group full">
          <label>Titel des Rezepts</label>
          <input type="text" bind:value={title} placeholder="z. B. Omas Kartoffelsuppe mit Würstchen" />
        </div>

        <div class="form-group">
          <label>Kategorie</label>
          <select bind:value={category}>
            <option value="Frühstück">🍳 Frühstück</option>
            <option value="Hauptmahlzeit">🍲 Hauptmahlzeit</option>
            <option value="Basics">🥪 Basics & Snacks</option>
          </select>
        </div>

        <div class="form-group">
          <label>Rating (1-5 Sterne)</label>
          <input type="number" min="1" max="5" bind:value={rating} />
        </div>

        <div class="form-group">
          <label>Zubereitungszeit (Minuten)</label>
          <input type="number" bind:value={prepTimeMin} />
        </div>

        <div class="form-group">
          <label>Kalorien / Portion (kcal)</label>
          <input type="number" bind:value={kcalPortion} />
        </div>

        <div class="form-group">
          <label>Protein / Portion (g)</label>
          <input type="number" bind:value={proteinPortion} />
        </div>

        <div class="form-group">
          <label>Standard Portionen</label>
          <input type="number" bind:value={portionen} />
        </div>

        <div class="form-group checkboxes full">
          <label class="checkbox-label">
            <input type="checkbox" bind:checked={batch} />
            📦 Batch Prep (Vorkochen / Meal Prep)
          </label>
          <label class="checkbox-label">
            <input type="checkbox" bind:checked={einfrierbar} />
            🧊 Einfrierbar
          </label>
        </div>
      </div>

      <!-- Zutaten / Checklist Editor -->
      <div class="section-box">
        <div class="section-header">
          <h3>🥗 Zutaten & Mengen (für Skalierungs-Schieberegler)</h3>
          <button class="btn-add" on:click={addIngredient}>+ Zutat hinzufügen</button>
        </div>

        {#each checklist as ing, i}
          <div class="ingredient-row">
            <input type="text" placeholder="Zutat (z. B. Kartoffeln)" bind:value={ing.name} class="ing-name" />
            <input type="number" placeholder="Menge" bind:value={ing.baseQty} class="ing-qty" />
            <input type="text" placeholder="Einheit (g, ml, Stk)" bind:value={ing.unit} class="ing-unit" />
            <button class="btn-remove" on:click={() => removeIngredient(i)}>🗑️</button>
          </div>
        {/each}
      </div>

      <!-- Schritte Editor -->
      <div class="section-box">
        <div class="section-header">
          <h3>👨‍🍳 Schritt-für-Schritt Zubereitung</h3>
          <button class="btn-add" on:click={addStep}>+ Schritt hinzufügen</button>
        </div>

        {#each steps as step, i}
          <div class="step-box">
            <div class="step-box-header">
              <span class="step-num">Schritt {i + 1}</span>
              <button class="btn-remove" on:click={() => removeStep(i)}>🗑️ Entfernen</button>
            </div>
            <input type="text" placeholder="Titel des Schritts (z. B. Gemüse schneiden (10 Min))" bind:value={step.header} class="step-input" />
            <textarea placeholder="Anweisung (z. B. Kartoffeln schälen und würfeln...)" bind:value={step.body} class="step-textarea"></textarea>
            
            <div class="step-extra-grid">
              <input type="text" placeholder="⚡ Parallel-Task (Optional: währenddessen Reis kochen)" bind:value={step.parallel} class="step-input" />
              <input type="number" placeholder="⏱️ Timer in Sekunden (z. B. 300 = 5 Min)" bind:value={step.timer} class="step-input" />
            </div>
          </div>
        {/each}
      </div>
    </div>

    <div class="modal-footer">
      <button class="btn-cancel" on:click={close}>Abbrechen</button>
      <button class="btn-save" on:click={handleSave}>Speichern 💾</button>
    </div>
  </div>
</div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    padding: 16px;
  }

  .modal-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    width: 100%;
    max-width: 720px;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
  }

  .modal-header {
    padding: 20px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #1e1916;
  }

  .modal-header h2 {
    font-size: 1.25rem;
    color: var(--accent-gold);
  }

  .btn-close {
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 1.5rem;
    cursor: pointer;
  }

  .modal-body {
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  .form-group.full {
    grid-column: 1 / -1;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .form-group label {
    font-size: 0.85rem;
    color: var(--text-muted);
  }

  .form-group input, .form-group select {
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    color: var(--text-main);
    padding: 10px;
    border-radius: 8px;
    font-size: 0.95rem;
  }

  .checkboxes {
    display: flex;
    gap: 20px;
    align-items: center;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-main);
    font-size: 0.9rem;
    cursor: pointer;
  }

  .section-box {
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    padding: 16px;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .section-header h3 {
    font-size: 0.95rem;
    color: var(--accent-gold);
  }

  .btn-add {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    color: var(--text-main);
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.8rem;
    cursor: pointer;
  }

  .btn-add:hover {
    border-color: var(--accent-gold);
  }

  .ingredient-row {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  .ing-name { flex: 2; background: var(--bg-card); border: 1px solid var(--border-color); color: var(--text-main); padding: 8px; border-radius: 6px; }
  .ing-qty { flex: 1; background: var(--bg-card); border: 1px solid var(--border-color); color: var(--text-main); padding: 8px; border-radius: 6px; }
  .ing-unit { flex: 1; background: var(--bg-card); border: 1px solid var(--border-color); color: var(--text-main); padding: 8px; border-radius: 6px; }

  .btn-remove {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 0.9rem;
    padding: 4px 8px;
  }

  .step-box {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .step-box-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .step-num {
    font-size: 0.85rem;
    font-weight: bold;
    color: var(--accent-gold);
  }

  .step-input {
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    color: var(--text-main);
    padding: 8px;
    border-radius: 6px;
    font-size: 0.9rem;
  }

  .step-textarea {
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    color: var(--text-main);
    padding: 8px;
    border-radius: 6px;
    font-size: 0.9rem;
    min-height: 60px;
    resize: vertical;
  }

  .step-extra-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 8px;
  }

  .modal-footer {
    padding: 16px 20px;
    border-top: 1px solid var(--border-color);
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    background: #1e1916;
  }

  .btn-cancel {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
  }

  .btn-save {
    background: var(--accent-gold);
    color: #181412;
    border: none;
    font-weight: bold;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
  }
</style>
