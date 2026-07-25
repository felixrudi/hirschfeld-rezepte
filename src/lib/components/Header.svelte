<script>
  export let activeTab = 'galerie';
  export let selectTab;
</script>

<header class="header">
  <div class="brand">
    <div class="brand-icon">🍳</div>
    <div class="brand-text">
      <h1>Hirschfeld Rezepte</h1>
      <p>KITCHEN OS & MEAL PREP SUITE</p>
    </div>
  </div>

  <nav class="nav-tabs">
    <button 
      class="tab-btn {activeTab === 'galerie' ? 'active' : ''}" 
      on:click={() => selectTab('galerie')}
    >
      🖼️ Galerie
    </button>

    <button 
      class="tab-btn {activeTab === 'fridge' ? 'active' : ''}" 
      on:click={() => selectTab('fridge')}
    >
      🍱 Kühlschrank & Reste
    </button>

    <button 
      class="tab-btn {activeTab === 'freezer' ? 'active' : ''}" 
      on:click={() => selectTab('freezer')}
    >
      🧊 Mein Tiefkühler
    </button>

    <button 
      class="tab-btn {activeTab === 'planer' ? 'active' : ''}" 
      on:click={() => selectTab('planer')}
    >
      📅 Wochenplaner
    </button>

    <button 
      class="tab-btn {activeTab === 'einkauf' ? 'active' : ''}" 
      on:click={() => selectTab('einkauf')}
    >
      🛒 Smart Einkaufsliste
    </button>
  </nav>
</header>

<style>
  .header {
    background: #1f1a17;
    border-bottom: 1px solid var(--border-color);
    padding: 16px 24px;
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    flex-wrap: wrap;
    gap: 16px;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .brand-icon {
    font-size: 28px;
    background: var(--accent-gold-glow);
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    border: 1px solid var(--accent-gold);
  }

  .brand-text h1 {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-main);
  }

  .brand-text p {
    font-size: 12px;
    color: var(--accent-gold);
    font-family: var(--font-mono);
  }

  .nav-tabs {
    display: flex;
    gap: 6px;
    background: #161210;
    padding: 4px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    flex-wrap: wrap;
  }

  .tab-btn {
    background: transparent;
    border: none;
    color: var(--text-muted);
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
    font-family: var(--font-body);
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s;
  }

  .tab-btn:hover {
    color: var(--text-main);
    background: rgba(255,255,255,0.05);
  }

  .tab-btn.active {
    background: var(--accent-gold);
    color: #161210;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(229, 164, 59, 0.3);
  }
</style>
