async function generate(){
const res = await fetch("/generate",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
job:job.value,
skills:skills.value
})
});
const data = await res.json();
result.innerText = data.text;
}

async function ats(){
const f = fileInput.files[0];
const form = new FormData();
form.append("resume",f);
form.append("job",jd.value);

const res = await fetch("/ats",{method:"POST",body:form});
const data = await res.json();
result.innerText = data.text;

progressBar.style.width = (Math.random()*40+60)+"%";
}

async function sendAnswer(){
const res = await fetch("/interview",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({answer:answer.value})
});
const data = await res.json();
chat.innerHTML += `<p>You: ${answer.value}</p><p>AI: ${data.reply}</p>`;
}

async function fixResume(){
const file = resumeFile.files[0];

if(file){
const form = new FormData();
form.append("resume",file);
const res = await fetch("/fix-resume-pdf",{method:"POST",body:form});
const data = await res.json();
fixedResume.innerText = data.fixed;
}else{
const res = await fetch("/fix-resume",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({resume:resumeText.value})
});
const data = await res.json();
fixedResume.innerText = data.fixed;
}
chat.innerHTML += `
  <div style="margin-top:10px;">
    <div style="color:#60a5fa;">You: ${answer.value}</div>
    <div style="color:#4ade80;">AI: ${data.reply}</div>
  </div>
`;
}
