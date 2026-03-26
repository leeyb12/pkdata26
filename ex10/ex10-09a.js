/* 참조복사 */
const arr = [11, 22, 33, 44, 55];
const arr2 = arr;
arr2[2] = 1004;
console.log(arr, arr2);
console.log(arr == arr2);
console.log(arr === arr2);

/* 옅은복사 */
const srr = [66, 77, 88, 99, 0];
const drr = [...srr];
drr[2] = 1004;
console.log(srr, drr);
console.log(srr == drr);
console.log(srr === drr);

console.log(Math.max(11, 22, 33, 44, 55, 66, 77, 88));
console.log(Math.max(arr));  // NaN
console.log(Math.max(...arr));
console.log(Math.min(...arr));