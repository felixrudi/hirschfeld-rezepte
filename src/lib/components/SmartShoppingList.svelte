<script>
  let deductStock = true;

  let deptFleisch = [
    { name: "500g Hähnchenbrustfilet (1 Packung)", inStock: true },
    { name: "4 Würstchen (Debreziner / Wiener)", inStock: true },
    { name: "5g Frischhefe (1 Würfel)", inStock: false }
  ];

  let deptGemuese = [
    { name: "1 kg Kartoffeln (1 Netz)", inStock: true },
    { name: "2 Bünde Suppengrün", inStock: true },
    { name: "1 rote Paprika", inStock: true }
  ];

  let deptVorrat = [
    { name: "500g Weizenmehl (Type 405)", inStock: false },
    { name: "100g Speisesalz", inStock: false },
    { name: "1 Dose Ananas in Stücken", inStock: true }
  ];

  function syncTodoist() {
    alert('🎉 Einkaufsliste erfolgreich mit Todoist synchronisiert!');
  }
</script>

<div class="shopping-wrapper">
  <div class="shopping-card">
    <div class="shopping-header">
      <div>
        <h2>🛒 Intelligente Einkaufsliste</h2>
        <p class="subtitle">Vorhandene Kühlschrank-Vorräte werden automatisch abgezogen!</p>
      </div>
      <button class="btn-action" on:click={syncTodoist}>Sync to Todoist 📲</button>
    </div>

    <div class="toggle-box">
      <label class="toggle-label">
        <input type="checkbox" bind:checked={deductStock} />
        <span>Kühlschrank-Vorräte automatisch von der Einkaufsliste ausblenden</span>
      </label>
    </div>

    <div class="dept-section">
      <h3>🥩 Fleisch & Frische</h3>
      {#each deptFleisch as item}
        {#if !deductStock || !item.inStock}
          <label class="shop-item">
            <input type="checkbox" />
            <span>{item.name}</span>
          </label>
        {/if}
      {/each}
    </div>

    <div class="dept-section">
      <h3>🥦 Gemüse & Obst</h3>
      {#each deptGemuese as item}
        {#if !deductStock || !item.inStock}
          <label class="shop-item">
            <input type="checkbox" />
            <span>{item.name}</span>
          </label>
        {/if}
      {/each}
    </div>

    <div class="dept-section">
      <h3>🥫 Vorrat & Konserven</h3>
      {#each deptVorrat as item}
        {#if !deductStock || !item.inStock}
          <label class="shop-item">
            <input type="checkbox" />
            <span>{item.name}</span>
          </label>
        {/if}
      {/each}
    </div>
  </div>
</div>

<style>
  .shopping-wrapper {
    max-width: 800px;
    margin: 0 auto;
  }

  .shopping-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 24px;
  }

  .shopping-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 12px;
  }

  .shopping-header h2 {
    font-size: 18px;
    font-weight: 700;
  }

  .subtitle {
    font-size: 13px;
    color: var(--accent-green);
    font-weight: 600;
  }

  .toggle-box {
    background: #191513;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid var(--border-color);
    margin-bottom: 20px;
  }

  .toggle-label {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
  }

  .toggle-label input {
    accent-color: var(--accent-gold);
  }

  .dept-section {
    margin-bottom: 20px;
  }

  .dept-section h3 {
    font-size: 13px;
    color: var(--accent-gold);
    text-transform: uppercase;
    margin-bottom: 10px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 4px;
  }

  .shop-item {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #191513;
    border: 1px solid var(--border-color);
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 6px;
    cursor: pointer;
  }

  .shop-item input {
    width: 18px;
    height: 18px;
    accent-color: var(--accent-gold);
  }

  .btn-action {
    background: var(--accent-gold-glow);
    border: 1px solid var(--accent-gold);
    color: var(--accent-gold);
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
  }
</style>
