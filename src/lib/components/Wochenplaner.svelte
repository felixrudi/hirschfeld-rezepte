<script>
  export let planDays = [
    {
      dayName: "Fr 24.07",
      meals: [
        { slot: "Frühstück", name: "Haferflocken + Whey" },
        { slot: "Mittag", name: "Nudelsalat ohne Mayonnaise", tag: "Gekocht" }
      ]
    },
    {
      dayName: "Sa 25.07",
      isToday: true,
      meals: [
        { slot: "Frühstück", name: "Haferflocken + Whey" },
        { slot: "Mittag", name: "Nudelsalat (Rest)", tag: "Reste" },
        { slot: "Abend 🍳 Kochen", name: "Hühnerfrikassee (1/4)", isCooking: true }
      ]
    },
    {
      dayName: "So 26.07",
      meals: [
        { slot: "Frühstück", name: "Tiramisu Oats (1/4)" },
        { slot: "Mittag 🧊 Aufwärmen", name: "Hühnerfrikassee (2/4)" }
      ]
    },
    {
      dayName: "Mo 27.07",
      meals: [
        { slot: "Frühstück", name: "Tiramisu Oats (2/4)" },
        { slot: "Mittag", name: "Hühnerfrikassee (3/4)" },
        { slot: "Abend 🍳 Kochen", name: "Hähnchen süß-sauer", isCooking: true }
      ]
    },
    {
      dayName: "Di 28.07",
      meals: [
        { slot: "Frühstück", name: "Tiramisu Oats (3/4)" },
        { slot: "Abend 🧊 Auftauen", name: "Hühnerfrikassee (aus Tiefkühler)", isFreezer: true }
      ]
    }
  ];
</script>

<div class="planer-wrapper">
  <div class="planer-header">
    <h2>📅 Wochenplaner (24.07. – 30.07.2026)</h2>
    <div class="target-badge">
      Ø Tages-Soll: <span class="gold">2.400 kcal</span> · <span class="green">150g Protein</span>
    </div>
  </div>

  <div class="plan-grid">
    {#each planDays as day}
      <div class="day-column">
        <div class="day-header">
          <span>{day.dayName}</span>
          {#if day.isToday}
            <span class="today-tag">Heute</span>
          {/if}
        </div>

        <div class="day-meals">
          {#each day.meals as meal}
            <div class="day-meal {meal.isCooking ? 'cooking' : ''} {meal.isFreezer ? 'freezer' : ''}">
              <div class="slot">{meal.slot}</div>
              <div class="name">{meal.name}</div>
            </div>
          {/each}
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .planer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 12px;
  }

  .planer-header h2 {
    font-size: 18px;
    font-weight: 700;
  }

  .target-badge {
    background: var(--bg-card);
    padding: 8px 16px;
    border-radius: 10px;
    border: 1px solid var(--border-color);
    font-size: 13px;
    font-family: var(--font-mono);
  }

  .target-badge .gold { color: var(--accent-gold); font-weight: 700; }
  .target-badge .green { color: var(--accent-green); font-weight: 700; }

  .plan-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
  }

  .day-column {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 16px;
  }

  .day-header {
    font-size: 16px;
    font-weight: 700;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .today-tag {
    font-size: 11px;
    background: var(--accent-gold);
    color: #161210;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 700;
  }

  .day-meals {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .day-meal {
    background: #191513;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 10px 12px;
  }

  .day-meal.cooking {
    border-color: var(--accent-gold);
  }

  .day-meal.freezer {
    border-color: var(--accent-blue);
  }

  .day-meal .slot {
    font-size: 11px;
    color: var(--accent-gold);
    font-weight: 600;
    text-transform: uppercase;
  }

  .day-meal .name {
    font-size: 14px;
    font-weight: 600;
    margin-top: 4px;
  }
</style>
