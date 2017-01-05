# lingualeo2anki

1. Запустите приложение
![2](https://cloud.githubusercontent.com/assets/7573215/8169784/8bf77b7a-13b4-11e5-9197-bbabf3e0143a.jpg)

2. Щелкните на любой из переводов, слово запишется в таблицу, а изображение загрузится в папку Anki с изображениями
![3](https://cloud.githubusercontent.com/assets/7573215/8169788/8e584a52-13b4-11e5-807b-39278da8b302.jpg)

3. После того, как сохраните все нужные слова, импортируйте их с помощью приложения Anki
![4](https://cloud.githubusercontent.com/assets/7573215/8169790/915372b8-13b4-11e5-8491-db89f9c141d2.jpg)

4. Разрешите использование HTML, и поставьте символ "|" разделителем полей (разделитель можно изменить)
![5](https://cloud.githubusercontent.com/assets/7573215/8169795/95baac40-13b4-11e5-82d6-ca4d6a986149.jpg)

5. Итоговый результат
![6](https://cloud.githubusercontent.com/assets/7573215/8169796/95c6b422-13b4-11e5-9727-7f548dcc01dd.jpg)


###Установка
1. Установить python и модули, используемые в приложении (requests, simplejson, pprintpp). Рекомендуется использовать pip для установки модулей.
2. Скачайте уже измененное [расширение](https://mega.co.nz/#F!8sFHjQZa!Tj0cZnarJo2N24SRFNWVMg) или измените его сами.
    > Сделайте копию C:\Users\\<имя пользователя>\AppData\Local\Google\Chrome\User Data\Default\Extensions\nglbhlefjhcjockellmeclkcijildjhi\\<версия>\. В файле lingualeo\js\server.js измените g+lingualeo.config.ajax.addWordToDict на "http://localhost:3000". Удалите папку _metadata.

3. Включите режим разработчика, добавьте расширение
![210601](https://cloud.githubusercontent.com/assets/7573215/8169794/959ce23c-13b4-11e5-8234-6f0c0429e440.png)
