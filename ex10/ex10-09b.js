function fn (...arr) {
  // 나머지 매개변수 ; py: (*args)
  console.log(arr, typeof arr);
  console.log(...arr);  // 전개연산자 ; py: fn[:]
}
fn(1, 2, 3, 4, 5, 6);