<script>
  export let leftovers = [];
  export let recipes = [];
  export let onCook;
  export let assignToPlan;

  let newLeftoverName = "";

  function addLeftover() {
    if (newLeftoverName.trim()) {
      leftovers = [
        ...leftovers, 
        { 
          id: Date.now(), 
          name: newLeftoverName.trim(), 
          count: 2, 
          cookedDate: new Date().toLocaleDateString('de-DE') 
        }
      ];
      newLeftoverName = "";
    }
  }

  let stockItems = [
    { name: "🥩 Hähnchenbrust (500g)", inStock: true },
    { name: "🫑 Rote Paprika", inStock: true },
    { name: "🍍 Dose Ananas", inStock: true },
    { name: "🥔 Kartoffeln (1 kg)", inStock: true },
    { name: "🌭 Würstchen (Debreziner)", inStock: true },
    { name: "🥕 Suppengrün (Karotte, Lauch)", inStock: true },
    { name: "🍚 Basmati Reis", inStock: false },
    { name: "🥛 Sahne / Kochsahne", inStock: false }
  ];

  function toggleItem(item) {
    item.inStock = !item.inStock;
    stockItems = [...stockItems];
  }
</script>

<div class="fridge-wrapper">
  <!-- BEREITS GEKOCHTE MAHLZEITEN & RESTE -->
  <div class="leftovers-box">
    <div class="leftovers-header">
      <div>
        <h2>🍱 Ready-to-Eat: Gekochte Reste im Kühlschrank</h2>
        <p>Trage gekochte Reste ein & übernehme sie per 1-Klick direkt in den Wochenplan:</p>
      </div>
      <div class="add-leftover-form">
        <input 
          type="text" 
          placeholder="Z. B. Chili Reste (2 Port.)..." 
          bind:value={newLeftoverName}
          on:keydown={(e) => e.key === 'Enter' && addLeftover()}
        />
        <button class="btn-action" on:click={addLeftover}>+ Reste eintragen</button>
      </div>
    </div>

    <div class="leftovers-grid">
      {#each leftovers as item}
        <div class="leftover-card">
          <div class="leftover-top">
            <span class="leftover-date">Gekocht am {item.cookedDate}</span>
            <span class="leftover-badge">{item.count} Portionen da</span>
          </div>
          <div class="leftover-name">{item.name}</div>
          <button 
            class="btn-action assign-btn" 
            on:click={() => assignToPlan(item.name, 'Sa Mittag')}
          >
            ➡️ In Wochenplan übernehmen (Sa Mittag)
          </button>
        </div>
      {/each}
    </div>
  </div>

  <!-- ROHWAREN & VORRAT -->
  <div class="fridge-container">
    <div class="fridge-sidebar">
      <h3>🧊 Rohwaren & Basis-Vorrat</h3>
      <p class="hint">Hake an, was du WIRKLICH im Kühlschrank hast:</p>
      
      <div class="stock-list">
        {#each stockItems as item}
          <label class="check-item {item.inStock ? 'checked' : ''}">
            <input 
              type="checkbox" 
              checked={item.inStock} 
              on:change={() => toggleItem(item)} 
            />
            <span>{item.name}</span>
          </label>
        {/each}
      </div>
    </div>

    <div class="matches-section">
      <div class="matches-header">
        <h2>🎯 100% Kochbar aus deinem Vorrat</h2>
        <span class="match-badge">2 Gerichte ohne Zukauf</span>
      </div>

      <div class="recipe-grid">
        {#each recipes.slice(0, 2) as recipe}
          <div class="recipe-card" on:click={() => onCook(recipe.id)}>
            <div class="card-banner" style="background-image: url('{recipe.image}');">
              <div class="card-badge green">✓ 100% Kochbar</div>
              <div class="card-category">{recipe.category}</div>
            </div>
            <div class="card-body">
              <div class="card-title">{recipe.title}</div>
              <p class="match-text">✓ Alle benötigten Hauptzutaten vorhanden!</p>
              <button class="btn-cook">Sofort Loskochen 👨‍🍳</button>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
</div>

<style>
  .fridge-wrapper { display: flex; flex-direction: column; gap: 24px; }
  .leftovers-box { background: var(--bg-card); border: 1px solid var(--accent-gold); border-radius: 16px; padding: 20px; }
  .leftovers-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 12px; }
  .leftovers-header h2 { font-size: 17px; font-weight: 700; color: var(--accent-gold); }
  .leftovers-header p { font-size: 13px; color: var(--text-muted); }

  .add-leftover-form { display: flex; gap: 8px; }
  .add-leftover-form input {
    background: #191513; border: 1px solid var(--border-color); border-radius: 8px; padding: 6px 12px; color: var(--text-main); font-size: 13px; outline: none;
  }

  .leftovers-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }
  .leftover-card { background: #191513; border: 1px solid var(--accent-green); border-radius: 12px; padding: 14px; }
  .leftover-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
  .leftover-date { font-size: 11px; color: var(--accent-green); font-weight: 600; }
  .leftover-badge { font-size: 11px; background: rgba(76, 175, 80, 0.2); color: var(--accent-green); padding: 2px 8px; border-radius: 10px; font-weight: 700; }
  .leftover-name { font-size: 15px; font-weight: 600; margin: 4px 0 10px 0; }
  .assign-btn { width: 100%; font-size: 12px; padding: 6px; }

  .fridge-container { display: grid; grid-template-columns: 320px 1fr; gap: 24px; }
  @media (max-width: 850px) { .fridge-container { grid-template-columns: 1fr; } }

  .fridge-sidebar { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; padding: 20px; }
  .fridge-sidebar h3 { font-size: 16px; font-weight: 700; margin-bottom: 4px; }
  .hint { font-size: 13px; color: var(--text-muted); margin-bottom: 14px; }

  .stock-list { display: flex; flex-direction: column; gap: 8px; }
  .check-item {
    display: flex; align-items: center; gap: 10px; background: #191513; border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 10px; cursor: pointer; user-select: none; transition: all 0.2s;
  }
  .check-item:hover { border-color: var(--accent-gold); }
  .check-item.checked { background: rgba(76, 175, 80, 0.1); border-color: var(--accent-green); color: var(--text-muted); }
  .check-item.checked span { text-decoration: line-through; }

  .matches-section h2 { font-size: 18px; font-weight: 700; }
  .matches-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
  .match-badge { font-size: 13px; color: var(--accent-gold); font-family: var(--font-mono); }

  .recipe-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
  .recipe-card { background: var(--bg-card); border: 1px solid var(--accent-green); border-radius: 16px; overflow: hidden; cursor: pointer; }
  .card-banner { height: 130px; background-size: cover; background-position: center; position: relative; }
  .card-badge.green { background: var(--accent-green); color: #fff; position: absolute; top: 12px; right: 12px; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 700; }
  .card-category { position: absolute; bottom: 12px; left: 12px; background: rgba(0,0,0,0.75); padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; color: #fff; text-transform: uppercase; }
  .card-body { padding: 16px; }
  .card-title { font-size: 16px; font-weight: 700; margin-bottom: 4px; }
  .match-text { font-size: 12px; color: var(--accent-green); font-weight: 600; margin-bottom: 12px; }
  .btn-cook { background: var(--accent-gold); color: #161210; padding: 8px; border: none; border-radius: 8px; font-weight: 700; width: 100%; cursor: pointer; }
  .btn-action { background: var(--accent-gold-glow); border: 1px solid var(--accent-gold); color: var(--accent-gold); border-radius: 8px; font-weight: 600; cursor: pointer; }
</style>
