let inp = prompt("값을 입력하세요.")
num = Number(inp) // * 1
console.log("(num = num + 1) + 순서");
console.log("후위연산자(num++)");
console.log(` num 값이 ${num}일때`);
console.log(`num++ 일때 ${num++}`);
console.log(`num++ 일때 ${num++}`);
console.log(`num++ 일때 ${num++}`);
console.log("===================");
num = Number(inp);  // 초기화
console.log("전위연산자(++num)");
console.log(` num 값이 ${num}일때`);
console.log(`++num 일때 ${++num}`);
console.log(`++num 일때 ${++num}`);
console.log(`++num 일때 ${++num}`);
console.log("===================");
num = Number(inp);  // 초기화
console.log("연속 테스트(++num, num++)");
console.log(` num 값이 ${num}일때`);
console.log(`num++ 일때 ${num++}`);
console.log(`++num 일때 ${++num}`);
console.log(`num-- 일때 ${num--}`);
console.log(`--num 일때 ${--num}`);
console.log("===================");