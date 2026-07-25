<script>
  export let recipe;
  export let onCook;
</script>

<div class="recipe-card" on:click={() => onCook(recipe.id)}>
  <div class="card-banner" style="background-image: url('{recipe.image}');">
    {#if recipe.batch}
      <div class="card-badge">🧊 Batch ×{recipe.portionen}</div>
    {/if}
    <div class="card-category">{recipe.category}</div>
  </div>

  <div class="card-body">
    <div class="card-title">{recipe.title}</div>
    <div class="card-rating">
      {'★'.repeat(recipe.rating)}{'☆'.repeat(5 - recipe.rating)} ({recipe.rating}.0)
    </div>

    <div class="card-stats">
      <div class="stat-item">
        <div class="val">{recipe.kcalPortion}</div>
        <div class="lbl">kcal</div>
      </div>
      <div class="stat-item">
        <div class="val">{recipe.proteinPortion}g</div>
        <div class="lbl">Protein</div>
      </div>
      <div class="stat-item">
        <div class="val">{recipe.prepTimeMin}m</div>
        <div class="lbl">Zeit</div>
      </div>
    </div>

    <button class="btn-cook">Rezept Kochen & Skalieren 👨‍🍳</button>
  </div>
</div>

<style>
  .recipe-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
  }

  .recipe-card:hover {
    transform: translateY(-4px);
    border-color: var(--accent-gold);
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
  }

  .card-banner {
    height: 140px;
    background-size: cover;
    background-position: center;
    position: relative;
    background-color: #332b25;
  }

  .card-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: rgba(26, 22, 20, 0.85);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    color: var(--accent-gold);
  }

  .card-category {
    position: absolute;
    bottom: 12px;
    left: 12px;
    background: rgba(0,0,0,0.75);
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    color: #fff;
    text-transform: uppercase;
  }

  .card-body {
    padding: 16px;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .card-title {
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 6px;
    color: var(--text-main);
  }

  .card-rating {
    color: var(--accent-gold);
    font-size: 13px;
    margin-bottom: 12px;
  }

  .card-stats {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
    background: #191513;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.05);
    text-align: center;
  }

  .stat-item .val {
    font-size: 14px;
    font-weight: 700;
    font-family: var(--font-mono);
  }

  .stat-item .lbl {
    font-size: 10px;
    color: var(--text-muted);
    text-transform: uppercase;
  }

  .btn-cook {
    background: var(--accent-gold);
    color: #161210;
    padding: 8px 16px;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    width: 100%;
    margin-top: 14px;
  }
</style>
