<script>
  export let freezerItems = [];
  export let assignToPlan;

  let newFreezerName = "";

  function addFreezerBatch() {
    if (newFreezerName.trim()) {
      freezerItems = [
        ...freezerItems,
        {
          id: Date.now(),
          name: newFreezerName.trim(),
          count: 3,
          date: new Date().toLocaleDateString('de-DE')
        }
      ];
      newFreezerName = "";
    }
  }
</script>

<div class="freezer-wrapper">
  <div class="freezer-box">
    <div class="freezer-header">
      <div>
        <h2>🧊 Mein Tiefkühler (Freezer Tracker)</h2>
        <p>Eingefrorene Batch-Portionen im Blick behalten & per 1-Klick zum Auftauen verplanen:</p>
      </div>

      <div class="add-form">
        <input 
          type="text" 
          placeholder="Z. B. Bolognese (3 Port.)..." 
          bind:value={newFreezerName}
          on:keydown={(e) => e.key === 'Enter' && addFreezerBatch()}
        />
        <button class="btn-blue" on:click={addFreezerBatch}>+ Batch einfrieren</button>
      </div>
    </div>

    <div class="freezer-grid">
      {#each freezerItems as item}
        <div class="freezer-card">
          <div class="freezer-top">
            <span class="freezer-date">Eingefroren am {item.date}</span>
            <span class="freezer-badge">🧊 {item.count} Dosen da</span>
          </div>
          <div class="freezer-name">{item.name}</div>
          <button 
            class="btn-blue assign-btn"
            on:click={() => assignToPlan(item.name + ' (Tiefkühl)', 'Di Abend')}
          >
            🧊 1 Dose Auftauen (Di Abend verplanen)
          </button>
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .freezer-box {
    background: var(--bg-card);
    border: 1px solid var(--accent-blue);
    border-radius: 16px;
    padding: 20px;
  }

  .freezer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 12px;
  }

  .freezer-header h2 {
    font-size: 17px;
    font-weight: 700;
    color: var(--accent-blue);
  }

  .freezer-header p {
    font-size: 13px;
    color: var(--text-muted);
  }

  .add-form {
    display: flex;
    gap: 8px;
  }

  .add-form input {
    background: #141a22;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 6px 12px;
    color: var(--text-main);
    font-size: 13px;
    outline: none;
  }

  .freezer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 14px;
  }

  .freezer-card {
    background: #141a22;
    border: 1px solid var(--accent-blue);
    border-radius: 12px;
    padding: 14px;
  }

  .freezer-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
  }

  .freezer-date {
    font-size: 11px;
    color: var(--accent-blue);
    font-weight: 600;
  }

  .freezer-badge {
    font-size: 11px;
    background: rgba(74, 144, 226, 0.2);
    color: var(--accent-blue);
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 700;
  }

  .freezer-name {
    font-size: 16px;
    font-weight: 600;
    margin: 6px 0 10px 0;
  }

  .btn-blue {
    background: rgba(74, 144, 226, 0.15);
    border: 1px solid var(--accent-blue);
    color: var(--accent-blue);
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }

  .btn-blue:hover {
    background: var(--accent-blue);
    color: #fff;
  }

  .assign-btn {
    width: 100%;
  }
</style>
