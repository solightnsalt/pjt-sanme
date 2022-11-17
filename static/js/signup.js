function doOpenCheck(chk) {
  var obj_pos = document.getElementsByName("job_pos");
  var obj = document.getElementsByName("job");
  for (var i = 0; i < obj.length; i++) {
    if (obj[i] != chk) {
      obj[i].checked = false;
      obj_pos[i].style.backgroundColor = "";
      obj_pos[i].style.color = "gray";
    } else {
      obj_pos[i].style.backgroundColor = "#03A63C";
      obj_pos[i].style.color = "white";
    }
  }
}

// 도메인 직접 입력 or domain option 선택
const domainListEl = document.querySelector("#domain-list");
const domainInputEl = document.querySelector("#domain-txt");
// select 옵션 변경 시
domainListEl.addEventListener("change", event => {
  // option에 있는 도메인 선택 시
  if (event.target.value !== "type") {
    // 선택한 도메인을 input에 입력하고 disabled
    domainInputEl.value = event.target.value;
    domainInputEl.readOnly = true;
    domainInputEl.style.backgroundColor = "white";
  } else {
    // 직접 입력 시
    // input 내용 초기화 & 입력 가능하도록 변경
    domainInputEl.value = "";
    domainInputEl.readOnly = false;
  }
});

const idValidation = document.querySelector("#id-check");
// const idVal = document.querySelector("#info__id");
const p = document.querySelector("#id-error");
const resultCheck = document.querySelector("#result-check");
idValidation.addEventListener("click", function (event) {
  event.preventDefault();
  const checkId = document.querySelector("#check_id");
  const regExp = /^[a-z0-9]{4,20}$/;
  if (!regExp.test(checkId.value)) {
    p.innerText = "아이디는 4~20자 영어 소문자, 숫자를 사용하세요.";
    p.style.color = "red";
  } else {
    p.innerText = "";
    axios({
      method: "get",
      url: "/accounts/signup/",
      params: {
        userId: `${checkId.value}`
      }
    }).then(response => {
      console.log(response);
      if (response.data.check) {
        p.innerText = "이미 등록된 아이디 입니다.";
        p.style.color = "red";
        checkId.value = "";
        resultCheck.value = 2;
      } else {
        p.innerText = "사용 가능한 아이디 입니다.";
        p.style.color = "green";
        resultCheck.value = 1;
      }
    }).catch(response => {
      console.log("경고");
    });
  }
});

const submitBtn = document.querySelector("#submitbtn");
const checkForm = document.querySelector("#form_check");
var checkJob = document.getElementsByName("job_pos");
submitBtn.addEventListener("click", function (event) {
  event.preventDefault();
  console.log(resultCheck.value);
  const checkId = document.querySelector("#check_id");
  const p = document.querySelector("#id-error");
  const p1 = document.querySelector("#pass_1");
  const p2 = document.querySelector("#pass_2");
  if (checkForm.check_id.value === "" || checkForm.password1.value === "" || checkForm.password2.value === "") {
    if (checkForm.check_id.value === "") {
      p.innerText = "아이디를 입력해 주세요.";
      p.style.color = "red";
      return checkId.focus();
    } else {
      p.innerText = "";
    }
    if (checkForm.password1.value === "") {
      p1.innerText = "비밀번호를 입력하세요.";
      p1.style.color = "red";
      p1.style.margin = "1rem 0 0 0";
      return checkForm.password1.focus();
    } else {
      p1.innerText = "";
    }
  } else {
    if (checkForm.password1.value !== checkForm.password2.value) {
      alert("비밀번호를 다시 확인해 주세요.");
    } else {
      if (resultCheck.value === undefined) {
        alert("아이디 중복 검사를 진행하세요.");
        idValidation.focus();
      } else if (resultCheck.value === 2) {
        alert("아이디를 다시 확인해 주세요.");
      } else {
        if (checkJob[0].style.color === "gray" && checkJob[1].style.color === "gray") {
          alert("직업을 선택해 주세요.");
        } else {
          resultCheck.disable = true;
          checkForm.submit();
        }
      }
    }
  }
});
