var tile = {
  letter: "-",
  left: 0,
  top: 0,
};

var tiles = new Array(7);
for (var i = 0; i < tiles.length; i++) {
  tiles[i] = new Array(3);
  tiles[i][0] = "-";
  tiles[i][1] = 0;
  tiles[i][2] = 0;
}
function drag_start(event) {
  var style = window.getComputedStyle(event.target, null);
  var str =
    parseInt(style.getPropertyValue("left")) -
    event.clientX +
    "," +
    (parseInt(style.getPropertyValue("top")) - event.clientY) +
    "," +
    event.target.id;
  event.dataTransfer.setData("Text", str);
}

function drop(event) {
  var offset = event.dataTransfer.getData("Text").split(",");
  var dm = document.getElementById(offset[2]);

  base1 = Math.round((event.clientX + parseInt(offset[0], 10) - 54.5) / 76.5);
  base2 = Math.round((event.clientY + parseInt(offset[1], 10) - 54.5) / 75.5);

  tiles[offset[2][2] - 1][0] = offset[2][0];
  tiles[offset[2][2] - 1][1] = base2;
  tiles[offset[2][2] - 1][2] = base1;

  dm.style.left = base1 * 76.5 + 54.5 + "px";
  dm.style.top = base2 * 75.5 + 54.5 + "px";

  event.preventDefault();
  return false;
}

function drag_over(event) {
  event.preventDefault();
  return false;
}

function sendTiles() {
  $.post("/nextMove", JSON.stringify(tiles), function (data, status) {
    status;
  });
}
