## :books: 프로젝트 주제
balbambalbam : korean-pronunciation-correction-system

> 세종대학교 2024-1 Capstone Design Project
> 
> 2024.01 ~ 2024.06

<br/><br/>

## 🏆 프로젝트 수상
✨ 세종대학교 창의설계경진대회 대상 ✨ 

✨ 세종대학교 2024 컴퓨터공학과 학술제 우수상 ✨ 

<br/><br/>

## :star2: 팀에서의 역할
📌 팀장
> 역할분담 및 회의 진행
>
> 프로젝트 발표

📌 인공지능
> 사용자 음성 분석 알고리즘 구축 및 시각화
>
> 서버 구축 및 http 통신 구현
> 
> ![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white">   <img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black"> 



<br/><br/>

## :star2: 프로젝트 배경
- 언어 학습에서 발음은 중요한 요소임

- 한국어 발음의 경우 발음하는 위치는 같지만 세기에 따라 달라지는 발음(ㅂ, ㅍ, ㅃ)이 존재

- 한국어 학습자의 급증

- 한국어 학습의 수요 대비 교육 공급의 부재

   

<br/><br/>

## :star2: 프로젝트 목적

- 언제 어디서나 반복 학습 가능한 발음 교정 피드백 시스템 제공

- 초기 사용자의 취약 음소를 판단하여 이를 집중적으로 개선할 수 있도록 함

- 커리큘럼 외에 자신이 원하는 문장 생성 및 학습이 가능하도록 함
  

<br/><br/>

## :star2: 프로젝트 기능
📌 발음 테스트 (사용자의 취약 음소 파악)
> 서울대학교 언어교육원 발음 진단지를 기반으로 최대 4개의 사용자 취약 음소 추출
>
> 학습 카드 리스트에서 붉은 색으로 시각화하여 사용자의 취약음 중점적 학습이 가능하도록 함

📌 학습 카드 (듣기-따라하기-피드백받기)
> 듣기 버튼을 눌러 해당 카드의 음성(사용자의 연령, 성별에 맞는 음성 합성) 듣기
>
> 마이크 버튼을 눌러 따라하기
>
> UI에 제시된 최대 5가지 피드백(사용자 음성 텍스트화, 발음 점수, 틀린 발음 학습 링크, 다시 듣기, Waveform)받기
>
> 위 세 단계의 반복을 통해 발음을 개선해 나아갈 수 있으며, 음절/단어/문장에 대한 단계별 카드를 통해 학습 가능

📌 학습 카드 생성 
> 커리큘럼 외의 학습을 할 수 있도록 사용자가 입력한 문장(단어)에 대한 학습 카드 제공
>
> 당장 활용해야 하는 발화(인삿말, 여행시 질문 등)를 사용자 개개인에 맞추어 학습할 수 있도록 함

<br/>

(앱 완성 결과, 배포 관련 정보는 [balbambalbam 공유 git](https://github.com/Capstone-4Potato)에서 확인)

<br/><br/>

## :star2: 프로젝트 개선사항
📌 STT API의 한계
> 문장 인식에 목적을 둔 Speech-to-Text API를 활용하였기에, 개별 음절에 대한 정확도가 좋지 못하다는 것을 느낌
> 
> 모델 학습을 통해 음성-텍스트 외에도 발음 기호를 추가 제공하는 등의 방법으로 개선할 수 있을 것으로 보임
