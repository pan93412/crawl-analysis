import streamlit as st
from modules.line import LineCrawler

print("LOADING, wait.")

lc = LineCrawler()

# text
st.button("Open LINE", on_click=lambda: lc.open_line())
group_name = st.text_input("Group name")
if st.button("Search group"):
    # result = lc.search_group(group_name)
    result = """2023.07.18 星期二
18:01 $Jarvis 不客氣~
2023.07.21 星期五
22:41 Old_Coder離開聊天
2023.07.31 星期一
18:48 _JelyFishhhhhh_離開聊天
2023.08.16 星期三
13:58 里克離開聊天
2023.08.22 星期二
14:33 William 午安各位
想拋出一個題目
和大家交流實務作法：
如何串聯在同一個請求中所產生的各個Log
（這些Log Statements可能是在不同Service Class內執行）
14:39 比比 用 session id 勒，摻在裡面再用這個 id 撈出來
14:42 山頂工程師 log 工具有包裝的話 應該 Singleton 方式設計的話 產生一個獨立 uuid
就可以確保都是同一個 request 產生的吧?
14:53 William Session ID 在前後端未分離時似乎可以
不過若是API的話呢？
14:54 William 似乎是一個方法
在Service Container生成一個全域Request ID
14:54 比比 api 同一個請求的 session 也會是同一個，如果要跟著使用者 那就加上使用者資訊
14:54 William 在呼叫Log函數時讀取並記錄
15:16 台南的小林 把所有的LOG丟到一個function   全部交給他來判斷是否累積  還是獨立建立一個資料
2023.08.24 星期四
19:48 EJ離開聊天
2023.09.03 星期日
00:08 marco加入聊天
00:08 Darren加入聊天
00:08 brbba加入聊天
2023.09.04 星期一
19:03 Frank Liu離開聊天
2023.09.13 星期三
21:23 LINN離開聊天
2023.09.14 星期四
01:36 Phy離開聊天
2023.09.21 星期四
09:00 Recca Chao 這邊似乎有點缺聊天動力ＸＤ
09:04 Foxy 0.0
10:55 顏小稀 這是我加入以來第一次有人講話XD
10:56 顏小稀 應該也是因為PHP有太多群了吧 都分散了
10:56 顏小稀 圖片
10:56 顏小稀 我自己就5個了
10:57 Foxy 第5個想回歸 可是對話的人好像也不多
10:57 Foxy 通常需要妹子問問題
10:59 顏小稀 那個最近也無聲....
11:01 顏小稀 比較起來vue群比較活躍一點，其它gcp或linebot都少量
11:05 新鮮的肝 原來還有這個社群
11:06 台南的小林 有問題的時候   才會活躍
12:44 小喵 我都在 Telegram 討論技術，反而這裡就比較少來了XDD
12:44 小喵 怎麼這麼多！！！
12:44 PHP是世界上最好的語言離開聊天
12:45 海力森 因為 PHP 的改版速度不如 JS？
12:45 小喵 圖片
12:45 小喵 結果我這邊也不少
12:49 始祖鳥 因為非本科比較往前端去吧
12:53 海力森 我就以 Vue 為主，Laravel 頂多就 CRUD、驗證和串 API 吧
12:58 Recca Chao @海力森 我還在等你專案的 GitHub repo 網址😆😆
12:59 Recca Chao 慢慢來吧 php 線下活動最近也有點低迷
13:00 Recca Chao 正在規劃中
13:03 海力森 我還沒上傳，不過倒是在 Azure DevOps 備份過網頁設計乙級術科的實作
13:24 始祖鳥 前端有一個布魯斯前端每天都超多討論
13:31 海力森 我也有加入
13:32 顏小稀 覺得台灣PHP要變時代眼淚 :~ 但國外還不錯
13:39 山頂工程師 因為大家都忙著在接案 和接公司的隕石 沒時間上來聊
13:40 山頂工程師 php 都偏這樣吧
13:42 比比 聽起來好像家庭代工 XD
13:43 Foxy 事實上應該都是
13:44 比比 搬零件回家 組好再交出去
13:45 顏小稀 還要會通靈
14:29 hoho離開聊天
16:36 比比 那我來問一個 laravel eloquent 的問題
```
    public static function boot()
    {
        parent::boot();
        static::updating(function ($model) {
            $model->createEditLog();
        });
        static::updated(function ($model) {
            $model->increment('version');
        });
    }
```
我的 updated 產生了無限迴圈，有什麼方法可以在這邊的 increment 不要觸發 updated 事件嗎
16:46 Darren 在$model->increment('version'); 加判斷吧 isDirty之類的

16:47 Darren 好像還要排除掉version的變動
16:48 比比 用 isDirty 的話，應該要放在 updating 比較合適？不然 updated 應該都會是 false
我來試試看
16:49 比比 如果 isDrity 會進判斷，那執行 increment 後也會繼續進去判斷式了
17:06 Darren 如果isDrity是空的或是只有isDrity(‘version’)就不進去執行increment
17:09 比比 原來如此！
17:13 EJLin 可以試試
static::withoutEvents(function () use ($model) {
    $model->increment('id');
});
2023.09.22 星期五
15:00 小喵 真ㄉ
2023.09.28 星期四
17:18 JmF離開聊天
2023.10.05 星期四
20:49 新手 - 橘子離開聊天
2023.10.06 星期五
22:33 AAAA離開聊天
2023.10.07 星期六
08:28 甲肉離開聊天
2023.10.15 星期日
18:11 柔伊離開聊天
21:31 GgLiu加入聊天
21:31 Kim加入聊天
21:31 Y8加入聊天
21:31 LaVida加入聊天
21:31 傻加入聊天
2023.10.18 星期三
08:46 JoJo離開聊天
2023.10.24 星期二
13:02 海力森離開聊天
2023.11.01 星期三
20:46 jaw離開聊天
2023.11.23 星期四
12:50 斬斬斬斬天地人 斷斷斷斷情仇恨 幫朋友代尋 Laravel Senior 兼職

Laravel 5+（使用 Blade），會接觸到 MSSQL, MySQL, PostgresSQL（至少要會操作其中二種）

主管：台灣人
時薪：新台幣 300-700 元/小時，依能力面議
工時：每週 20+ 小時
產業：白產（行銷 / 政府 / 電商 / 傳產）
薪資: 每月結算，可用台幣現金發放或 USDT

工作內容：評估需求 -> 確認時數 -> 審核後開工 -> 後續須處理 BUG 修復

有興趣聯絡我，帳號 i..r.e...s.c.o...n.s.u.l..t.i.n.g（去掉 .）
14:15 Encore PHP 8.3今天推出了耶，我反而覺得改版好快
14:44 台南的小林 5.6跳到7.1之間有段很長的時間，7.1開始就更新很快了
14:46 比比 畢竟有個未出世的 6
14:48 斬斬斬斬天地人 斷斷斷斷情仇恨 更新快好啊
14:51 斬斬斬斬天地人 斷斷斷斷情仇恨 .net python node java 每個都更新得像飛的一樣
14:57 小喵 官網最新的文章是 PHP 8.3.0 RC 6 available for testing
看起來還沒 stable?
15:06 Recca Chao Java 還好吧
15:06 Recca Chao Java 8 鐵打不動
15:17 Encore已收回訊息
17:08 jia加入聊天
17:08 小黑加入聊天
2023.11.24 星期五
07:27 Encore PHP8.3 Download 出來了,是stable!
https://www.php.net/downloads.php
2023.11.25 星期六
19:20 Richard離開聊天
2023.12.04 星期一
10:41 TH離開聊天
2023.12.05 星期二
13:16 晚安離開聊天
2023.12.20 星期三
01:37 York加入聊天
01:37 php自學中加入聊天
01:37 苗栗酸辣醬加入聊天
15:10 York離開聊天
15:56 Nana加入聊天
2023.12.21 星期四
18:05 Recca Chao 大家好，2023 年末，歡迎大家一起來聊聊 php 和 Laravel 的未來

https://events.laravel-dojo.com/events/46-laravel-2023-%E6%AD%B2%E6%9C%AB%E5%B0%8F%E8%81%9A
20:02 小喵 期待 Laravel 11 搭配 PHP 8.3 可以迸出一些火花來
20:02 小喵 最近正在想要把手邊的專案從 CodeIgniter 4 Port 到 Laravel 10 但又怕 Laravel 11 要出了
20:24 Darren 不用怕，每年都一版新的，怎麼跟都跟不到
20:28 比比 真的 大膽一點 不要怕 反正每年都在升級 總是要面對的
22:00 小毛網站 98goto.com 不想面對(moon laugh)
22:00 Chad Peng 他更新速度很快 別等
22:02 小毛網站 98goto.com 有些客戶還在PHP 5.4-5.6 (翻白眼)
22:27 番茄蛋炒飯 5.4-5.6升級建議砍掉重練嗎🤣
22:41 台南的小林 我也遇到一個5.6的   真是很煩
22:50 小毛網站 98goto.com 版本不可怕…功能多 經手過N手 還有一堆隱藏功能的那種(moon laugh)
22:54 斬斬斬斬天地人 斷斷斷斷情仇恨 我現在 Laravel 6 要準備搬家了
22:55 斬斬斬斬天地人 斷斷斷斷情仇恨 也是頭有點痛，還好我 PHP 已經上 7 了
2023.12.22 星期五
12:05 php自學中離開聊天
15:26 Recca Chao 感覺大家更新的還是沒辦法很順利到 8
"""
    if result is None:
        st.error("No such group.")
    else:
        st.text_area("Content", result, height=200)
        parsed = lc._parse_chat(result)
        st.write(parsed)
