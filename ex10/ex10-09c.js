const a = [1, 2];
const b = [3, 4];
const c = a + b;
const result = [...a, ...b];
console.log(c);
console.log(result);
console.log(typeof c, Array.isArray(c));
console.log(typeof result, Array.isArray(result));