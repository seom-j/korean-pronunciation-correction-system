
# 🌰 음성 합성 모델, Tacotron2 🌰

>  본 Tacotron2는 Attention 기반 Seq-to-Seq TTS 모델 구조를 지니고 있으며, <문장/음성>쌍만으로 별도의 작업 없이 학습 가능한 End-to-End 모델이다. 24.6시간 한 사람의 음성, 영어 기준 MOS 약 4.5의 높은 점수를 획득하였다. 즉, 합성 품질이 뛰어나다. 

 
>  우리는 본 프로젝트를 위해 aihub의 '뉴스 대본 및 앵커 음성 데이터'와 '다화자 음성합성 데이터'를 사용하였다. 학습한 음성마다의 모델은 ckpt 파일 내에 존재한다. 

<br/><br/>

## ⚙️ 모델 inference 방법 ⚙️

#### 🔸 필요한 패키지 설치
> pip install -r requirements.txt

<br/>

#### 🔸 inference 파일 수정
> inference.py 안의 문장 목록에 원하는 문장 써넣기

<br/>

#### 🔸 모델 체크포인트를 활용한 음성 생성
> 여성 청년 목소리 합성
> 
> python inference.py -t ckpt/tc2_ckpt_w_02/tc2_130000.ckpt -w ckpt/wg_ckpt_w_02/wg_390000.ckpt

> 남성 청년 목소리 합성
> 
> python inference.py -t ckpt/tc2_ckpt_m_02/tc2_130000.ckpt -w ckpt/wg_ckpt_m_02/wg_390000.ckpt

