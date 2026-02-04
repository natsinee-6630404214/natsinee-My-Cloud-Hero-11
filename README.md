# natsinee-My-Cloud-Hero-11
Name: Natsinee Seangchan 
Student ID: 663040421-4

# การทำงาน
จากโจทย์ ได้ทำการสร้างโฟลเดอร์เพิ่ม ชื่อ historical_court ซึ่งมีการทำงานโดยรวมของระบบ ดังนี้
1. เมื่อรันโปรแกรม Agent ตัวแรกจะถามผู้ใช้ว่าอยากวิเคราะห์บุคคล/เหตุการณ์อะไร
2. ระบบจะส่งหัวข้อนั้นเข้าสู่ “ศาลประวัติศาสตร์”
3. มีการสืบค้น 2 ฝั่งพร้อมกัน:
   - ฝั่งด้านบวก
   - ฝั่งด้านลบ/ข้อโต้แย้ง
4. ผู้พิพากษา(Judge Agent) จะตรวจว่าข้อมูลสมดุลหรือไม่
5. ถ้ายังไม่สมดุล ทำการวนลูปค้นข้อมูลเพิ่ม
6. เมื่อข้อมูลครบทั้งสองด้าน จะทำการเขียนรายงานสรุปแบบเป็นกลางลงไฟล์

# โครงสร้างของ Agent
court_clerk (Root Agent) → historical_court (SequentialAgent) → trial_loop (LoopAgent) → investigation_team (ParallelAgent) → admirer_agent, critic_agent → judge_agent → file_writer

# หน้าที่ของแต่ละ Agent
# court_clerk (Root Agent)
- คุยกับผู้ใช้
- ถามหัวข้อทางประวัติศาสตร์
- เก็บข้อมูลไว้ใน state ชื่อ `topic`
- ส่งงานต่อให้ระบบศาล
# admirer_agent
- ค้นข้อมูล “ด้านบวก”
- เช่น ความสำเร็จ ผลงาน คุณูปการ
- ใช้ Wikipedia tool
- บันทึกข้อมูลใน state ชื่อ `pos_data`
# critic_agent
- ค้นข้อมูล “ด้านลบ”
- เช่น ความล้มเหลว ข้อวิจารณ์ ความขัดแย้ง
- บันทึกใน state ชื่อ `neg_data`
# investigation_team (ParallelAgent)
ทำให้ admirer_agent และ critic_agent ทำงานพร้อมกัน เพื่อให้ได้ข้อมูลสองฝั่งในเวลาเดียวกัน
# judge_agent
- เปรียบเทียบข้อมูลฝั่งบวกและลบ
- ถ้าฝั่งใดน้อยเกินไป → ให้ระบบวนค้นใหม่
- ถ้าข้อมูลสมดุล → ใช้ tool `exit_loop` เพื่อจบลูป
# trial_loop (LoopAgent)
ควบคุมการทำงานแบบวนซ้ำ จะวนจนกว่า Judge จะพอใจ หรือครบจำนวนรอบที่กำหนด (ซึ่งในที่นี้กำหนด max_iterations = 3)
# file_writer
- เขียนรายงานสรุปแบบ “คำตัดสินศาล”
- เป็นกลาง ไม่เลือกข้าง
- บันทึกเป็นไฟล์ .txt

# แนวคิดเทคนิคที่ใช้
- SequentialAgent: ควบคุมลำดับการทำงานหลัก 
- ParallelAgent: ค้นข้อมูลสองฝั่งพร้อมกัน 
- LoopAgent: วนค้นข้อมูลจนสมดุล 
- State Management: แชร์ข้อมูลระหว่าง Agent 
- Tool Usage: Wikipedia + เขียนไฟล์ 
- exit_loop tool: ใช้จบลูปอย่างเป็นทางการ 


# วิธีรันโปรแกรม
adk run historical_court

# ตัวอย่างการทำ
ในที่นี้พิมพ์ "I’d like to know about King Naresuan and his role in Thai history." ไป ซึ่งผลลัพธ์สุดท้ายจะถูกบันทึกที่ output/verdict.txt
<img width="1918" height="1021" alt="image" src="https://github.com/user-attachments/assets/079d8083-d272-4315-aee0-6f3fcc1a0717" />
<img width="1919" height="1016" alt="Screenshot 2026-02-04 230839" src="https://github.com/user-attachments/assets/06bc9b15-6944-4943-8e1f-61ac45f77c50" />




