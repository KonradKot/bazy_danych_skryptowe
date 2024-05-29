class Samochod {
    constructor(marka, model, rokProdukcji, pojemnoscSilnika, cena) {
        this.marka = marka;
        this.model = model;
        this.rokProdukcji = rokProdukcji;
        this.pojemnoscSilnika = pojemnoscSilnika;
        this.cena = cena;
    }

    wyswietlSzczegoly() {
        console.log(`${this.marka} ${this.model} ${this.rokProdukcji} ${this.cena}`);
    }

    srednieSpalanie() {
        if (this.pojemnoscSilnika < 1.0) {
            return 5;
        } else if (this.pojemnoscSilnika >= 1.0 && this.pojemnoscSilnika < 1.3) {
            return 5 + Math.floor(this.rokProdukcji / 850);
        } else {
            return 8;
        }
    }
}

const marki = ["Toyota", "Ford", "BMW", "Audi", "Mercedes"];
const modele = ["Corolla", "Focus", "X5", "A4", "C-Class"];
const lataProdukcji = [2015, 2018, 2019, 2017, 2020];
const pojemnosciSilnika = [1.2, 1.5, 2.0, 1.8, 2.2];
const ceny = [50000, 60000, 70000, 80000, 90000];

// Tworzenie tablicy obiektów reprezentujących samochody
let samochody = [];
for (let i = 0; i < 5; i++) {
    const samochod = new Samochod(marki[i], modele[i], lataProdukcji[i], pojemnosciSilnika[i], ceny[i]);
    samochody.push(samochod);
}

console.log("Szczegoly samochodow:");
for (const samochod of samochody) {
    samochod.wyswietlSzczegoly();
    console.log(`Srednie spalanie: ${samochod.srednieSpalanie()} litrow/100km`);
}

// Funkcja porównująca samochody
function porownajSamochody(samochod1, samochod2) {
    if (samochod1.pojemnoscSilnika > samochod2.pojemnoscSilnika) {
        return `${samochod1.marka} ${samochod1.model} jest wiekszy.`;
    } else if (samochod1.pojemnoscSilnika < samochod2.pojemnoscSilnika) {
        return `${samochod2.marka} ${samochod2.model} jest wiekszy.`;
    } else {
        if (samochod1.rokProdukcji > samochod2.rokProdukcji) {
            return `${samochod1.marka} ${samochod1.model} jest wiekszy.`;
        } else if (samochod1.rokProdukcji < samochod2.rokProdukcji) {
            return `${samochod2.marka} ${samochod2.model} jest większy.`;
        } else {
            return "Oba samochody sa identyczne pod wzgledem pojemnosci silnika i roku produkcji.";
        }
    }
}

// Porównanie 3 par samochodów
console.log("\nPorownanie samochodow:");
console.log(porownajSamochody(samochody[0], samochody[1]));
console.log(porownajSamochody(samochody[2], samochody[3]));
console.log(porownajSamochody(samochody[1], samochody[4]));

// Funkcja tworząca słownik z danymi samochodów
function stworzSlownik(poleTablicy) {
    const slownik = {};
    for (const samochod of samochody) {
        if (poleTablicy === "marka") {
            if (!slownik[samochod.marka]) {
                slownik[samochod.marka] = [];
            }
            slownik[samochod.marka].push(samochod);
        } else if (poleTablicy === "model") {
            if (!slownik[samochod.model]) {
                slownik[samochod.model] = [];
            }
            slownik[samochod.model].push(samochod);
        } else if (poleTablicy === "rok") {
            if (!slownik[samochod.rokProdukcji]) {
                slownik[samochod.rokProdukcji] = [];
            }
            slownik[samochod.rokProdukcji].push(samochod);
        } else if (poleTablicy === "pojemnosc") {
            if (!slownik[samochod.pojemnoscSilnika]) {
                slownik[samochod.pojemnoscSilnika] = [];
            }
            slownik[samochod.pojemnoscSilnika].push(samochod);
        } else if (poleTablicy === "cena") {
            if (!slownik[samochod.cena]) {
                slownik[samochod.cena] = [];
            }
            slownik[samochod.cena].push(samochod);
        }
    }
    return slownik;
}

// Wyświetlenie słownika z danymi samochodów
console.log("\nSlownik samochodow wedlug pola 'marka':");
console.log(stworzSlownik("marka"));