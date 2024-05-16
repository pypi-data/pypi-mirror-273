from icare_nlp.task_disp import TaskDisp

task_disp=TaskDisp()

user_query="可以確認下有冇糖不甩？"
print('\n\n')
print(user_query)
task_disp.intent_classify(user_query)

user_query="可唔可以概括下今时嘅周边嗎？"
print('\n\n')
print(user_query)
task_disp.intent_classify(user_query)

user_query="microwave喺我手嘅邊個方向？"
print('\n\n')
print(user_query)
task_disp.intent_classify(user_query)


user_query="呢啲QR 碼中邊個係折扣優惠券？"
print('\n\n')
print(user_query)
task_disp.intent_classify(user_query)

user_query="糖醋排骨卖几多？"
print('\n\n')
print(user_query)
task_disp.intent_classify(user_query)

user_query="你能唔能夠幫我分析下呢個QR code裏面嘅資料？"
print('\n\n')
print(user_query)
task_disp.intent_classify(user_query)

