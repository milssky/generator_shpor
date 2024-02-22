let saying = [
    ["Гордый полагается на память, мудрый - на памятку.", "Салон Прекрасный, греческий философ"], 
    ["Когда хочешь блеснуть — демонстрируй хорошую память. Когда хочешь действовать — загляни в хорошую шпаргалку.", "Притон Финикийский, греческий философ"], 
    ["Мудрец знает: шпаргалка хранит, а человек - действует.", "Аль\' Горитм, персидский просветитель"], 
    ["Истинный самурай в руках держит меч, в уме — цель, а в шпаргалке — знания.", "Кодекс Буши До, первая редакция"], 
    ["Мудрый учитель Хо одобряет шпаркалки.", "Мудрый учитель Хо"], 
    ["С хорошей шпаргалкой лучше, чем без вообще шпаргалки.", "φανερότης, греческий капитан"], 
];


document.addEventListener('DOMContentLoaded', function() {
    var randomSaying = saying[Math.floor(Math.random() * saying.length)];

    let textBlock = document.getElementById('footer');
    let sayingText = textBlock.querySelectorAll('#saying .text');
    let sayingSrc = textBlock.querySelectorAll('#saying .src');

    sayingText[0].innerHTML = randomSaying[0];
    sayingSrc[0].innerHTML = randomSaying[1];
 }, false);









