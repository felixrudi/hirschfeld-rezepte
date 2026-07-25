<script>
  import Header from './lib/components/Header.svelte';
  import RecipeCard from './lib/components/RecipeCard.svelte';
  import KitchenStepperModal from './lib/components/KitchenStepperModal.svelte';
  import FridgeTracker from './lib/components/FridgeTracker.svelte';
  import FreezerTracker from './lib/components/FreezerTracker.svelte';
  import Wochenplaner from './lib/components/Wochenplaner.svelte';
  import SmartShoppingList from './lib/components/SmartShoppingList.svelte';

  import { initialRecipes, initialLeftovers, initialFreezerItems } from './lib/recipesData.js';

  let isAuthenticated = typeof window !== 'undefined' && (
    localStorage.getItem('food_auth') === 'true' || 
    document.cookie.includes('food_auth=true')
  );
  let passwordInput = '';
  let authError = false;

  function checkPassword() {
    if (
      passwordInput === '@qDDWnshCWujuSCb#w!z0xvQEC$y^0@$dRHWEH' ||
      passwordInput === 'hirschfeld2026' || 
      passwordInput === 'hirschfeld'
    ) {
      isAuthenticated = true;
      localStorage.setItem('food_auth', 'true');
      // Set 1-Year (365 Days) Persistent Cookie for mobile devices
      document.cookie = "food_auth=true; max-age=31536000; path=/; sameSite=Lax; secure";
      authError = false;
    } else {
      authError = true;
    }
  }

  let recipes = initialRecipes;
  let leftovers = initialLeftovers;
  let freezerItems = initialFreezerItems;

  let activeTab = 'galerie';
  let activeRecipeId = null;

  $: activeRecipe = recipes.find(r => r.id === activeRecipeId);

  function selectTab(tabId) {
    activeTab = tabId;
  }

  function handleCook(recipeId) {
    activeRecipeId = recipeId;
  }

  function closeModal() {
    activeRecipeId = null;
  }

  function assignToPlan(itemName, targetSlot) {
    alert(` Success: "${itemName}" wurde direkt für [${targetSlot}] im Wochenplan eingetragen!`);
    activeTab = 'planer';
  }

  let searchQuery = "";
  let activeChip = "all";

  $: filteredRecipes = recipes.filter(r => {
    const matchesSearch = r.title.toLowerCase().includes(searchQuery.toLowerCase());
    let matchesChip = true;

    if (activeChip === "protein") matchesChip = r.tags.includes("protein");
    if (activeChip === "quick") matchesChip = r.tags.includes("quick");
    if (activeChip === "freeze") matchesChip = r.tags.includes("freeze");

    return matchesSearch && matchesChip;
  });
</script>

<div class="app-container">
  {#if !isAuthenticated}
    <div class="auth-overlay">
      <div class="auth-card">
        <div class="auth-icon">🔒</div>
        <h2>Hirschfeld Rezepte</h2>
        <p>Bitte Passwort eingeben, um fortzufahren:</p>
        <div class="auth-form">
          <input 
            type="password" 
            placeholder="Passwort..." 
            bind:value={passwordInput}
            on:keydown={(e) => e.key === 'Enter' && checkPassword()}
          />
          <button class="btn-auth" on:click={checkPassword}>Freischalten 🔑</button>
        </div>
        {#if authError}
          <div class="auth-error">❌ Falsches Passwort</div>
        {/if}
      </div>
    </div>
  {:else}
    <Header {activeTab} {selectTab} />

    <main class="main-content">
    {#if activeTab === 'galerie'}
      <div class="filter-toolbar">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input 
            type="text" 
            placeholder="Rezept oder Zutat suchen..." 
            bind:value={searchQuery}
          />
        </div>

        <div class="filter-chips">
          <button 
            class="chip {activeChip === 'all' ? 'active' : ''}" 
            on:click={() => activeChip = 'all'}
          >
            Alle ({recipes.length})
          </button>
          <button 
            class="chip {activeChip === 'protein' ? 'active' : ''}" 
            on:click={() => activeChip = 'protein'}
          >
            💪 High Protein
          </button>
          <button 
            class="chip {activeChip === 'quick' ? 'active' : ''}" 
            on:click={() => activeChip = 'quick'}
          >
            ⚡ Schnell (&lt;30m)
          </button>
          <button 
            class="chip {activeChip === 'freeze' ? 'active' : ''}" 
            on:click={() => activeChip = 'freeze'}
          >
            🧊 Einfrierbar
          </button>
        </div>
      </div>

      <div class="recipe-grid">
        {#each filteredRecipes as recipe}
          <RecipeCard {recipe} onCook={handleCook} />
        {/each}
      </div>
    {:else if activeTab === 'fridge'}
      <FridgeTracker 
        {leftovers} 
        {recipes} 
        onCook={handleCook} 
        {assignToPlan} 
      />
    {:else if activeTab === 'freezer'}
      <FreezerTracker 
        {freezerItems} 
        {assignToPlan} 
      />
    {:else if activeTab === 'planer'}
      <Wochenplaner />
    {:else if activeTab === 'einkauf'}
      <SmartShoppingList />
    {/if}
  </main>

  {#if activeRecipe}
    <KitchenStepperModal 
      recipe={activeRecipe} 
      onClose={closeModal} 
    />
  {/if}
  {/if}
</div>

<style>
  .auth-overlay {
    position: fixed;
    inset: 0;
    background: #14100e;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    padding: 20px;
  }

  .auth-card {
    background: var(--bg-card);
    border: 1px solid var(--accent-gold);
    border-radius: 20px;
    padding: 36px 32px;
    max-width: 400px;
    width: 100%;
    text-align: center;
    box-shadow: 0 16px 48px rgba(0,0,0,0.8);
  }

  .auth-icon {
    font-size: 42px;
    margin-bottom: 12px;
  }

  .auth-card h2 {
    font-size: 22px;
    font-weight: 700;
    color: var(--accent-gold);
    margin-bottom: 6px;
  }

  .auth-card p {
    font-size: 14px;
    color: var(--text-muted);
    margin-bottom: 20px;
  }

  .auth-form {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .auth-form input {
    background: #191513;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 12px 16px;
    color: var(--text-main);
    font-size: 15px;
    text-align: center;
    outline: none;
  }

  .auth-form input:focus {
    border-color: var(--accent-gold);
  }

  .btn-auth {
    background: var(--accent-gold);
    color: #161210;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
  }

  .auth-error {
    color: var(--accent-red);
    font-size: 13px;
    font-weight: 600;
    margin-top: 14px;
  }

  .app-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .main-content {
    flex: 1;
    max-width: 1280px;
    width: 100%;
    margin: 0 auto;
    padding: 24px;
  }

  .filter-toolbar {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 24px;
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    align-items: center;
    justify-content: space-between;
  }

  .search-box {
    flex: 1;
    min-width: 260px;
    position: relative;
  }

  .search-box input {
    width: 100%;
    background: #191513;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 10px 16px 10px 40px;
    color: var(--text-main);
    font-size: 14px;
    outline: none;
  }

  .search-icon {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
  }

  .filter-chips {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .chip {
    background: #191513;
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }

  .chip.active {
    background: var(--accent-gold-glow);
    border-color: var(--accent-gold);
    color: var(--accent-gold);
    font-weight: 600;
  }

  .recipe-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
    gap: 20px;
  }
</style>
