# Mysql Proxy


Mysql Proxy



Hibernate Shards'in tamamlanmasini beklerken, ve uygulama kodlamasina baslamadan once alternatif bazi seceneklere bakmaya basladik. Isleyecegimiz seceneklerden biri Mysql Proxy, ve genel olarak bu tur yazilimlar uzerinden SQL veri tabanlarina baglanirken proxy'lerin nasil kullanilacagi.Proxy ne ise yarar? Proxy, yer tutucu anlaminda, servis tarafindaki bir 'sey' ile ona 'baglanan' arasina gecen ve aracilik rolunu ustlenen bir ara program/katmandir. Bu ara programa baglaninca servisteki seye baglanmis gibi olursunuz.Bunun faydalarindan biri, ara katmanda ek bazi islemleri yapabilir hale gelmektedir. Yani SQL proxy'leri bir veri tabaniymis gibi size bir servis sunarlar. Proxy'ler bunu ya JDBC seviyesinde, pur Java kodu ile, ya da tamamen DB yerine gecerek SQL seviyesinde yapiyorlar.MySQL sirketinin kendi yazdigi, kendi database'leri icin hazirladigi proxy programi MySQL Proxy. Bu programi kurup, arka planda hangi veri tabanini (ya da tabanlari -host ve db ismi ile beraber-) yansitmasi gerektigini soyluyorsunuz ve Mysql Proxy bu arkadaki tabanlar icin bir gecis noktasi oluyor. Bunun yatay olcekleme, sharding ile alakasi surada: Bu ara katmanlar SELECT, INSERT gibi komutlarin icine bakarak, o komutu veri icerigine gore belli bir 'shard'a yonlendirme isini de yapabilir. Bu durumda Java katmaninin Hibernate Shards'a ihtiyaci kalmaz, cunku yonlendirme isi JDBC'nin bile ruhunun duymadigi baska bir katmanda yapilacaktir. JDBC, MySQL'e konustugunu zannedecektir halbuki MySQL Proxy ile konusur olacaktir, onun uzerinden belli bir database'e yonlendirilecektir - Hibernate ve Java bununla alakadar olmayacaktir. Tabii onceden belirttigimiz gibi, yazilim mimarisi ve veriye erisim "stili" Hibernate kullanim seviyesinde 'sharded'   kavramina hazir olacak, o baska. Iliskilere, vs. dikkat edilecek filan. Fakat bunlar yine pur Java/Hibernate seviyesindeki dikkat edilmesi gerekenler.MySQL Proxy ilginc bir program: Bu programin kendisini de 'kodlamaniz' mumkun bir kere - Lua adinda bir programlama dilini destekliyor. Belli noktalara cengel (hook) koyulmus ve bu cengellere sizin programiniz takilabiliyor, ve iste o ara noktada istediginiz ek taklalari atabiliyorsunuz. O zaman SELECT icerigine bakip yonlendirme isi bir Lua programi olacak. Simdiden mevcut bir Lua programi, mesela, "yazim icin master'a okuma icin slave'e gitme" isini kodlamis. MySQL sitesinde paylasilan kodlardan biri. Pek cok diger kodlar var.Sonuclari buradan paylasiriz. Testler devam ediyor.



