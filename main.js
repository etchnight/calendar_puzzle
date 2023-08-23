"use strict";
const fs = require("fs");
const bottomPlate = [
  [0, 0, 0, 0, 0, 0, 9],
  [0, 0, 0, 0, 0, 0, 9],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 9, 9, 9, 9],
];

const pieces = [
  [
    [1, 1, 1],
    [1, 1, 1],
  ],
  [
    [2, 2, 2],
    [2, 2, 0],
  ],
  [
    [3, 0, 0],
    [3, 0, 0],
    [3, 3, 3],
  ],
  [
    [4, 4, 4],
    [4, 0, 4],
  ],
  [
    [5, 0, 0],
    [5, 5, 5],
    [0, 0, 5],
  ],
  [
    [6, 6, 6, 0],
    [0, 0, 6, 6],
  ],
  [
    [7, 7, 7, 7],
    [0, 0, 7, 0],
  ],
  [
    [8, 8, 8, 8],
    [0, 0, 0, 8],
  ],
];

function rotate(arr) {
  let newArr = buildArr(arr[0].length, arr.length);
  for (let i = 0; i < arr.length; i++) {
    for (let j = 0; j < arr[0].length; j++) {
      newArr[j][arr.length - 1 - i] = arr[i][j];
      //console.log(`${i},${j}=>${j},${arr.length - 1 - i}`);
    }
  }
  return newArr;
}
function flip(arr) {
  let newArr = buildArr(arr.length, arr[0].length);
  for (let i = 0; i < arr.length; i++) {
    for (let j = 0; j < arr[0].length; j++) {
      newArr[i][arr[0].length - 1 - j] = arr[i][j]; //左右翻转
    }
  }
  return newArr;
}
function buildAList(arr) {
  let aList = [arr, flip(arr)];
  for (let i = 0; i < 3; i++) {
    let newArr = rotate(arr);
    aList.push(newArr);
    aList.push(flip(newArr));
    arr = newArr;
  }
  let newAList = [];
  for (let item of aList) {
    let itemAdded = newAList.find((e) => {
      return JSON.stringify(e) === JSON.stringify(item);
    });
    if (!itemAdded) {
      newAList.push(item);
    }
  }
  return newAList;
}
function buildArr(maxi, maxj) {
  let arr = [];
  for (let i = 0; i < maxi; i++) {
    arr.push([]);
    for (let j = 0; j < maxj; j++) {
      arr[i].push(0);
    }
  }
  return arr;
}
function isSame(arr1, arr2) {
  if (arr1.length != arr2.length) {
    return false;
  }
  if (arr1[0].length != arr2[0].length) {
    return false;
  }
  if (arr1.toString() != arr2.toString()) {
    return false;
  }
  console.log(JSON.stringify(arr1), JSON.stringify(arr2));
  return true;
}
function buildPieces() {
  let resultList = [];
  for (let piece of pieces) {
    let result = buildAList(piece);
    resultList.push(result);
  }
  fs.writeFileSync("pieces.json", `${JSON.stringify(resultList)}`, {
    flag: "w+",
    encoding: "utf-8",
  });
  return;
}

function locate(arr, bottomPlate, i, j) {
  let result = structuredClone(bottomPlate);
  if (arr.length + i > bottomPlate.length) {
    return null;
  }
  if (arr[0].length + j > bottomPlate[i].length) {
    return null;
  }
  for (let row = 0; row < arr.length; row++) {
    for (let col = 0; col < arr[0].length; col++) {
      if (arr[row][col] * bottomPlate[row + i][col + j]) {
        return null;
      }
      result[row + i][col + j] += arr[row][col];
    }
  }
  return result;
}
function main() {//遍历算法，结果太多
  let pieces = fs.readFileSync("pieces.json", { encoding: "utf-8" });
  pieces = JSON.parse(pieces);
  //let result = locate(pieces[0][0], 4, 4);
  let resultList = [structuredClone(bottomPlate)];
  console.time("a");
  let piecesIndex = 0;
  for (piecesIndex = 0; piecesIndex < pieces.length; piecesIndex++) {
    let pieceList = pieces[piecesIndex];
    resultList = locateAll(pieceList, resultList);
    console.timeLog("a");
  }
  console.timeEnd("a");
  fs.writeFileSync("result.json", json.stringify(resultList), {
    encoding: "utf-8",
    flag: "w+",
  });
  console.log("结束");
  return;
  function locateAll(pieceList, resultList) {
    let resultListNew = [];
    for (let result of resultList) {
      for (let index = 0; index < pieceList.length; index++) {
        let piece = pieceList[index];
        for (let i = 0; i < 7; i++) {
          for (let j = 0; j < 7; j++) {
            let resultNew = locate(piece, result, i, j);
            if (!resultNew) {
              continue;
            } else {
              console.log(
                `将第${piecesIndex}种碎片的第${index}种状态放在位置${i}，${j}上`
              );
              resultListNew.push(resultNew);
            }
          }
        }
      }
    }
    return resultListNew;
  }
}
function main(index1,index2){
  let pieces = fs.readFileSync("pieces.json", { encoding: "utf-8" });
  pieces = JSON.parse(pieces);
  let result = [structuredClone(bottomPlate)];
}
main();
