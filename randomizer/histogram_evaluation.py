text = """lap: 0, time:32.18650000000000
lap: 1, time:81.67657423019409
lap: 2, time:131.5286886692047
lap: 3, time:179.4567267894745
lap: 4, time:228.09031200408936
lap: 5, time:274.1659035682678
lap: 6, time:325.76457142829895
lap: 7, time:377.58107113838196
lap: 8, time:423.3396167755127
lap: 9, time:476.68967604637146
lap: 10, time:527.4219660758972
lap: 11, time:574.1041646003723
lap: 12, time:620.7860310077667
lap: 13, time:670.7179210186005
lap: 14, time:719.4009146690369
lap: 15, time:766.393128156662
lap: 16, time:816.0909299850464
lap: 17, time:865.9047930240631
lap: 18, time:914.0913274288177
lap: 19, time:967.1448132991791
lap: 20, time:1015.2473485469818
lap: 21, time:1065.7706623077393
lap: 22, time:1113.0094118118286
lap: 23, time:1160.5834262371063
lap: 24, time:1208.2133786678314
lap: 25, time:1258.9921867847443
lap: 26, time:1307.1666042804718
lap: 27, time:1355.0814554691315
lap: 28, time:1403.8298926353455
lap: 29, time:1455.314198732376
lap: 30, time:1502.6349799633026
lap: 31, time:1553.3120377063751
lap: 32, time:1601.0550155639648
lap: 33, time:1647.6809186935425
lap: 34, time:1693.8213529586792
lap: 35, time:1739.8623704910278
lap: 36, time:1789.8394832611084
lap: 37, time:1834.967122554779
lap: 38, time:1881.3690111637115
lap: 39, time:1932.5533819198608
lap: 40, time:1982.2276451587677
lap: 41, time:2029.7339777946472
lap: 42, time:2077.529886484146
lap: 43, time:2126.661150455475
lap: 44, time:2173.4493539333344
lap: 45, time:2218.9750163555145
lap: 46, time:2269.904658317566
lap: 47, time:2314.9213314056396
lap: 48, time:2364.3279314041138
lap: 49, time:2413.2551403045654
lap: 50, time:2460.3848798274994
lap: 51, time:2509.1866850852966
lap: 52, time:2557.277070760727
lap: 53, time:2602.0688314437866
lap: 54, time:2650.212373495102
lap: 55, time:2696.7449400424957
lap: 56, time:2743.98002576828
lap: 57, time:2794.653080224991
lap: 58, time:2846.0316712856293
lap: 59, time:2897.3458321094513
lap: 60, time:2945.37953042984
lap: 61, time:2992.2750742435455
lap: 62, time:3040.2012588977814
lap: 63, time:3089.567646741867
lap: 64, time:3137.0919857025146
lap: 65, time:3186.2984747886658
lap: 66, time:3235.360856294632
lap: 67, time:3283.2878720760345
lap: 68, time:3332.5995559692383
lap: 69, time:3378.314108848572
lap: 70, time:3426.2063794136047
lap: 71, time:3477.054132938385
lap: 72, time:3538.2552230358124
lap: 73, time:3584.46497130394
lap: 74, time:3632.5716195106506
"""
a = text.split("\n")[:-1]
print(a)
b = [string.split(",")[1] for string in a]
print(b)
c = [float(string[6:14]) for string in b]
print(c)
d = []
for index in range(len(c) - 1):
    print(index)
    d.append(c[index + 1]-c[index])
for index, item in enumerate(d):
    print(index, item)
