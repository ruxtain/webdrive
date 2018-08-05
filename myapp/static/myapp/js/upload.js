const realFileBtn = document.getElementById("id_files");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");
const customSubmit = document.getElementById("custom-submit");
const realSubmit = document.getElementById("real-submit");
customBtn.addEventListener("click", function() {
  realFileBtn.click(); 
});
customSubmit.addEventListener("click", function() {
    realSubmit.click();
});
// 一旦添加文件，value（文件路径）就改变了，于是拿这个值
realFileBtn.addEventListener("change", function() {
  if (realFileBtn.value) {
    // 用正则筛选出文件的 basename 注意要包含中文
    // customTxt.innerHTML = realFileBtn.value.match(/[\/\\]([\u4e00-\u9fa5\w\d\s\.\+\-(\)]+)$/)[1];
    customTxt.innerHTML = realFileBtn.value.replace("C:\\fakepath\\", '');
  } else {
    customTxt.innerHTML = "未选择任何文件";
  }
});