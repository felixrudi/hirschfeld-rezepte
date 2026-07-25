export const initialRecipes = [
  {
    id: "kartoffelsuppe",
    title: "Omas Kartoffelsuppe mit Würstchen",
    category: "Hauptmahlzeit",
    rating: 5,
    prepTimeMin: 35,
    kcalPortion: 420,
    proteinPortion: 18,
    batch: true,
    portionen: 4,
    einfrierbar: true,
    image: "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=600&q=80",
    tags: ["protein", "quick", "freeze"],
    baseIngredientName: "Kartoffeln",
    baseIngredientQty: 1000,
    unit: "g",
    checklist: [
      { name: "Kartoffeln (vorwiegend festkochend)", baseQty: 1000, unit: "g" },
      { name: "Suppengrün (Karotten, Sellerie, Lauch)", baseQty: 500, unit: "g" },
      { name: "Gemüsebrühe", baseQty: 1000, unit: "ml" },
      { name: "Sahne (oder Kochsahne)", baseQty: 100, unit: "ml" },
      { name: "Würstchen (Debreziner / Frankfurter)", baseQty: 4, unit: "Stück" },
      { name: "Olivenöl, Zwiebel, Knoblauch, Gewürze", baseQty: 1, unit: "Satz" }
    ],
    steps: [
      {
        header: "Gemüseschnippeln & Vorbereiten (10 Min)",
        body: "1 kg Kartoffeln schälen und in ca. 2 cm Würfel schneiden. Suppengrün putzen: Karotten & Sellerie würfeln, Lauch in Ringe schneiden. 1 Zwiebel & 1 Knoblauchzehe fein hacken.",
        parallel: null,
        timer: null
      },
      {
        header: "Anschwitzen im Suppentopf (5 Min)",
        body: "2 EL Olivenöl in einem großen Topf erwärmen. Zwiebel & Knoblauch 3 Min glasig dünsten. Kartoffeln & Suppengrün dazugeben und 3-5 Min mitanbraten für Röstaromen.",
        parallel: null,
        timer: 300
      },
      {
        header: "Ablöschen & Köcheln lassen (15-20 Min)",
        body: "Mit 1 Liter Gemüsebrühe ablöschen, Abdecken und bei mittlerer Hitze sanft köcheln lassen, bis das Gemüse butterweich ist.",
        parallel: "⚡ PARALLEL JETZT ERLEDIGEN: Während die Suppe köchelt, schnei die 4 Würstchen in dünne Scheiben und messe 100 ml Sahne ab!",
        timer: 900
      },
      {
        header: "Stampfen, Würstchen ziehen lassen & Servieren (5 Min)",
        body: "Topf vom Herd nehmen. Suppe nach Wunsch anpürieren oder grob anstampfen. Sahne & Würstchenscheiben dazugeben und 5 Min ziehen lassen. Mit Salz, Pfeffer & Muskat abschmecken!",
        parallel: "⚡ PARALLEL ERLEDIGEN: Tisch decken & Suppenteller anwärmen.",
        timer: 300
      }
    ]
  },
  {
    id: "haehnchen",
    title: "Hähnchen süß-sauer",
    category: "Hauptmahlzeit",
    rating: 5,
    prepTimeMin: 30,
    kcalPortion: 340,
    proteinPortion: 31,
    batch: true,
    portionen: 4,
    einfrierbar: true,
    image: "https://images.unsplash.com/photo-1525755662778-989d0524087e?auto=format&fit=crop&w=600&q=80",
    tags: ["protein", "quick", "freeze", "eggfree"],
    baseIngredientName: "Hähnchenbrustfilet",
    baseIngredientQty: 500,
    unit: "g",
    checklist: [
      { name: "Hähnchenbrustfilet", baseQty: 500, unit: "g" },
      { name: "Rote Paprika", baseQty: 1, unit: "Stück" },
      { name: "Karotte", baseQty: 1, unit: "Stück" },
      { name: "Dose Ananas in Stücken (mit Saft)", baseQty: 360, unit: "g" },
      { name: "Speisestärke", baseQty: 4, unit: "EL" },
      { name: "Basmati Reis (roh)", baseQty: 240, unit: "g" },
      { name: "Sojasauce, Essig, Tomatenmark, Sesamöl", baseQty: 1, unit: "Satz" }
    ],
    steps: [
      {
        header: "Schnippeln & Einlegen (10 Min)",
        body: "500g Hähnchenbrust in mundgerechte Würfel schneiden. Paprika & Karotte würfeln. Ananas abtropfen lassen (Saft auffangen!). Hähnchen mit 1 EL Sojasauce & 1 EL Wasser benetzen und in 2 EL Stärke wenden.",
        parallel: null,
        timer: null
      },
      {
        header: "Sauce anrühren & Reis aufsetzen (5 Min)",
        body: "Ananassaft mit 6 EL Essig, 2 EL Tomatenmark, 2 EL Sojasauce & 2 EL Zucker verrühren. 1 EL Stärke einrühren.",
        parallel: "⚡ PARALLEL JETZT ERLEDIGEN: 240g Reis mit 480ml leicht gesalzenem Wasser aufsetzen und bei kleiner Hitze 15 Min köcheln lassen!",
        timer: 900
      },
      {
        header: "Hähnchen knusprig braten (7 Min)",
        body: "1 EL Öl im Wok/Pfanne stark erhitzen. Hähnchenwürfel 5-7 Minuten scharf anbraten, bis sie leicht braun und knusprig sind. Herausnehmen.",
        parallel: null,
        timer: 420
      },
      {
        header: "Gemüse anbraten, Sauce einkochen & Servieren (5 Min)",
        body: "Paprika, Karotte & Ananas 3 Min Pfannenrühren. Sauce & Hähnchen dazugeben, 2 Min köcheln lassen bis die Sauce andickt. Zusammen mit dem fertigen Reis servieren!",
        parallel: null,
        timer: 300
      }
    ]
  },
  {
    id: "pizzateig",
    title: "Pizzateig wie beim Italiener",
    category: "Basics",
    rating: 5,
    prepTimeMin: 30,
    kcalPortion: 446,
    proteinPortion: 13,
    batch: true,
    portionen: 4,
    einfrierbar: true,
    image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=600&q=80",
    tags: ["freeze", "eggfree"],
    baseIngredientName: "Weizenmehl",
    baseIngredientQty: 500,
    unit: "g",
    checklist: [
      { name: "Weizenmehl (Type 405 oder 00)", baseQty: 500, unit: "g" },
      { name: "Lauwarmes Wasser", baseQty: 300, unit: "ml" },
      { name: "Frischhefe", baseQty: 5, unit: "g" },
      { name: "Salz", baseQty: 2, unit: "TL" }
    ],
    steps: [
      {
        header: "Hefe auflösen & Kneten (15 Min)",
        body: "5g Frischhefe im lauwarmen Wasser auflösen. Mehl & Salz in eine Schüssel geben, Wasser-Hefe-Gemisch hinzugießen und 10–12 Minuten kräftig kneten.",
        parallel: null,
        timer: 600
      },
      {
        header: "Teig ruhen lassen (60 Min)",
        body: "Teig abdecken und an einem warmen Ort 1–2 Stunden gehen lassen, bis sich das Volumen verdoppelt hat.",
        parallel: "⚡ PARALLEL ERLEDIGEN: Tomatensauce anrühren & Mozzarella reiben.",
        timer: 3600
      }
    ]
  },
  {
    id: "overnight_oats",
    title: "Tiramisu Overnight Oats",
    category: "Frühstück",
    rating: 5,
    prepTimeMin: 15,
    kcalPortion: 380,
    proteinPortion: 24,
    batch: true,
    portionen: 4,
    einfrierbar: false,
    image: "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=600&q=80",
    tags: ["quick", "protein"],
    baseIngredientName: "Haferflocken",
    baseIngredientQty: 200,
    unit: "g",
    checklist: [
      { name: "Haferflocken", baseQty: 200, unit: "g" },
      { name: "Magertopfen / Magerquark", baseQty: 400, unit: "g" },
      { name: "Espresso (gebrüht)", baseQty: 150, unit: "ml" },
      { name: "Chiasamen", baseQty: 20, unit: "g" },
      { name: "Kakaopulver zum Bestreuen", baseQty: 10, unit: "g" }
    ],
    steps: [
      {
        header: "Oats anrühren & Schichten (15 Min)",
        body: "Haferflocken mit gekühltem Espresso & Milch verrühren. In 4 Gläser füllen. Magerquark mit etwas Süße glattrühren und als Top-Schicht verteilen. Mit Kakaopulver bestreuen und über Nacht kühlen.",
        parallel: null,
        timer: 900
      }
    ]
  }
];

export const initialLeftovers = [
  { id: 1, name: "Nudelsalat ohne Mayonnaise", count: 2, cookedDate: "24.07.2026" },
  { id: 2, name: "Hühnerfrikassee (Batch)", count: 3, cookedDate: "25.07.2026" }
];

export const initialFreezerItems = [
  { id: 101, name: "Hühnerfrikassee (Batch × 4)", count: 3, date: "25.07.2026" },
  { id: 102, name: "Linsen-Bolognese (Batch × 3)", count: 2, date: "21.07.2026" }
];
