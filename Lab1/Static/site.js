function zoomImage(image) {
    var modal = document.getElementById("modal");
    var modalImg = document.getElementById("zoomedImage");
    var captionText = document.getElementById("caption");

    var div = document.getElementById("modal-image");

    modal.style.display = "block";
    div.style.display = "block";
    modalImg.src = image.src;
    captionText.innerHTML = image.alt;
}

function showOrderMessage() {
    var modal = document.getElementById("modal");
    var div = document.getElementById("modal-text");

    modal.style.display = "block";
    div.style.display = "block";
}

function closeModal() {
    var modal = document.getElementById("modal");
    var image = document.getElementById("modal-image");
    var text = document.getElementById("modal-text");
    modal.style.display = "none";
    image.style.display = "none";
    text.style.display = "none";
}


function buy(id) {
    var div = document.getElementById(id + "-number");
    $.post("buy", {phone_id: id, number: div.innerHTML}, function () {
        location.href = 'home';
    });
}

function remove(id) {
    $.post("remove", {phone_id: id}, function () {
        location.href = 'order';
    });
}

function completeOrder() {
    $.post("complete", {}, function () {
        location.href = 'home';
    });
}

function producerChecked(id, item) {
    $.post("producer", {producer: id, state: item.checked}, function () {
        location.href = 'home';
    });
}
function operations_systemChecked(id, item) {
    $.post("operation_systems", {operations_system: id, state: item.checked}, function () {
        location.href = 'home';
    });
}
function type_phoneChecked(id, item) {
    $.post("type_phone", {type: id, state: item.checked}, function () {
        location.href = 'home';
    });
}
function multimediaChecked(id, item) {
    $.post("multimedia", {multimedia: id, state: item.checked}, function () {
        location.href = 'home';
    });
}
function costChanged(parameter, value) {
    $.post("cost", {parameter: parameter, value: value}, function () {
        location.href = 'home';
    });
}

function inc(id) {
    var div = document.getElementById(id + "-number");
    if (div.innerHTML * 1 < 99)
        div.innerHTML = div.innerHTML * 1 + 1;
}

function dec(id) {
    var div = document.getElementById(id + "-number");
    if (1 < div.innerHTML * 1)
        div.innerHTML = div.innerHTML * 1 - 1;
}
// endregion Main page