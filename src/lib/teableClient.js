const TEABLE_BASE_URL = "https://teable.hirschfeld.at/api";
const TEABLE_TABLE_REZEPTE = "tblcbq85gOIz1CPGKY7";
const TEABLE_TABLE_KUEHLSCHRANK = "tblEIxC113727puUCsZ";
const TEABLE_TABLE_TIEFKUEHLER = "tblIEIOKrTMpk0znBKE";
const TEABLE_TABLE_WOCHENPLAN = "tblbiKt8nyyZnVx63Vg";

export async function fetchTeableRecipes(token) {
  if (!token) return [];
  try {
    const res = await fetch(`${TEABLE_BASE_URL}/table/${TEABLE_TABLE_REZEPTE}/record`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.records || []).map(r => ({
      id: r.id,
      title: r.fields.Titel,
      category: r.fields.Kategorie || 'Hauptmahlzeit',
      rating: r.fields.Rating || 5,
      prepTimeMin: r.fields.Zubereitung_Min || 30,
      kcalPortion: r.fields.Kcal_Portion || 400,
      proteinPortion: r.fields.Protein_Portion || 20,
      batch: r.fields.Batch || false,
      portionen: r.fields.Portionen || 4,
      einfrierbar: r.fields.Einfrierbar || false,
      quelle: r.fields.Quelle || ''
    }));
  } catch (err) {
    console.error('Teable fetch error:', err);
    return [];
  }
}
