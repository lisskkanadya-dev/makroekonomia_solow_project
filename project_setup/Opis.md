# Opis projektu: test modelu Solowa i konwergencji

## Treść zadania

**Zadanie empiryczne: test modelu Solowa i konwergencji**

Celem zadania jest przygotowanie kodu w Pythonie, który automatycznie pobiera dane empiryczne i sprawdza, czy obserwujemy mechanizmy przewidywane przez model Solowa.

Program powinien:

- pobrać dane o PKB per capita dla wybranych krajów,
- obliczyć średnie tempo wzrostu w badanym okresie,
- sprawdzić beta-konwergencję, czyli czy biedniejsze kraje rosły szybciej,
- sprawdzić sigma-konwergencję, czyli czy różnice dochodowe między krajami malały,
- przedstawić wyniki na wykresach i sformułować wnioski.

Pytanie badawcze:

> Czy dane empiryczne potwierdzają przewidywania modelu Solowa dotyczące konwergencji?

## Idea modelu Solowa

Model Solowa jest jednym z podstawowych modeli wzrostu gospodarczego. W uproszczeniu pokazuje, że kraje mogą zbliżać się do swojego długookresowego poziomu dochodu. Jeżeli biedniejszy kraj ma podobne warunki instytucjonalne, technologię, stopę oszczędności i wzrost ludności jak bogatszy kraj, to może rosnąć szybciej, ponieważ łatwiej mu nadrabiać zaległości.

Nie oznacza to jednak, że wszystkie kraje zawsze automatycznie doganiają bogatsze gospodarki. Wynik zależy od wybranej grupy krajów, okresu analizy, jakości danych oraz wielu czynników gospodarczych i politycznych.

## Beta-konwergencja

Beta-konwergencja oznacza sytuację, w której kraje o niższym początkowym PKB per capita rosną szybciej niż kraje bogatsze.

W projekcie sprawdzamy to przez porównanie:

- początkowego poziomu PKB per capita,
- średniego rocznego tempa wzrostu w badanym okresie.

Jeżeli na wykresie kraje biedniejsze mają wyższe tempo wzrostu, a współczynnik regresji jest ujemny, to jest to argument za występowaniem beta-konwergencji.

## Sigma-konwergencja

Sigma-konwergencja oznacza zmniejszanie się różnic dochodowych między krajami w czasie.

W projekcie mierzymy ją przez odchylenie standardowe logarytmu PKB per capita w każdym roku. Jeżeli ta miara spada, oznacza to, że kraje stają się do siebie bardziej podobne pod względem dochodu per capita.

Jeżeli sigma rośnie, różnice dochodowe między krajami zwiększają się.

## Jak czytać wykresy

### 1. Wykres PKB per capita w czasie

Ten wykres pokazuje, jak zmieniał się poziom PKB per capita w poszczególnych krajach. Można zobaczyć, które kraje startowały z wyższego poziomu i które rozwijały się szybciej.

### 2. Wykres beta-konwergencji

Na osi poziomej znajduje się początkowy poziom PKB per capita w skali logarytmicznej. Na osi pionowej znajduje się średnie roczne tempo wzrostu.

Interpretacja:

- linia nachylona w dół sugeruje beta-konwergencję,
- linia nachylona w górę sugeruje brak beta-konwergencji,
- punkty daleko od linii pokazują kraje, które zachowywały się nietypowo względem trendu.

### 3. Wykres sigma-konwergencji

Ten wykres pokazuje, czy zróżnicowanie dochodów między krajami malało czy rosło.

Interpretacja:

- spadek linii oznacza zmniejszanie różnic dochodowych,
- wzrost linii oznacza zwiększanie różnic dochodowych,
- brak wyraźnego trendu oznacza, że nie ma jednoznacznych dowodów na sigma-konwergencję.

## Jak interpretować wyniki

Wyniki należy interpretować ostrożnie.

Jeżeli program pokaże ujemny współczynnik beta i spadek sigmy, można powiedzieć, że w badanej grupie krajów i w badanym okresie dane wspierają hipotezę konwergencji.

Jeżeli beta jest dodatnia albo sigma rośnie, oznacza to, że dane nie potwierdzają prostej wersji hipotezy konwergencji.

Możliwa jest też sytuacja mieszana, na przykład:

- występuje beta-konwergencja, ale nie ma sigma-konwergencji,
- biedniejsze kraje rosły szybciej, ale różnice dochodowe nadal się nie zmniejszyły wystarczająco.

## Ograniczenia analizy

Ta analiza jest uproszczona.

Najważniejsze ograniczenia:

- wykorzystujemy tylko PKB per capita,
- wynik zależy od wyboru krajów,
- wynik zależy od początku i końca badanego okresu,
- dane mogą mieć braki,
- model Solowa jest modelem teoretycznym i nie obejmuje wszystkich czynników rozwoju,
- analiza nie dowodzi przyczynowości, tylko pokazuje zależności w danych.

Dlatego wnioski należy traktować jako ilustrację empiryczną, a nie jako pełne badanie naukowe.
