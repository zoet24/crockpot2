// Plus minus button
document.addEventListener('click', (e) => {
    if (!e.target.closest('.btn-plus-minus__input')) return;

    const num = e.target.closest('.btn-plus-minus__btn').querySelector('.btn-plus-minus__num');
    var numVal = parseInt(num.value);

    const minVal = num.getAttribute("min");
    const maxVal = num.getAttribute("max");
    const step = parseInt(num.getAttribute("step"));

    const isPlus = e.target.closest('.btn-plus-minus__input--plus');
    const isMinus = e.target.closest('.btn-plus-minus__input--minus');
    const isViewRecipe = e.target.closest('.view-recipe');

    if ((isPlus !== null) && (numVal < maxVal)) {
        numVal += step;
    }

    if ((isMinus !== null) && (numVal > minVal)) {
        numVal -= step;
    }

    num.value = numVal;

    if (isViewRecipe !== null) {
        multiplyIngs(numVal);
    }
});

// If on the same page as view recipe, change quantity of food
function multiplyIngs(numVal) {
    const targetNums = document.querySelectorAll('.btn-plus-minus__targetNum');
    const ingNums = document.querySelectorAll('.btn-plus-minus__ingNum');

    for (var i = 0; i < targetNums.length; i++) {
        var targetNum = targetNums[i];
        var ingNum = parseFloat(ingNums[i].innerHTML);
        var targetNumNew = ingNum * numVal;

        targetNum.innerHTML = targetNumNew;
    }
}