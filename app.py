import time
import asyncio
from datetime import datetime, timedelta
import pytz
import discord
from discord.ext import commands

# Botの初期設定
intents = discord.Intents.default()
intents.members = True  # メンバー管理のため
intents.message_content = True  # メッセージ内容のIntentを有効化
bot = commands.Bot(command_prefix="!", intents=intents)

# 日本時間のタイムゾーンを取得
japan_tz = pytz.timezone('Asia/Tokyo')

# ロールIDのリスト（順番通り）
role_ids = [
    "ここにIDを貼り付け",  
    "ここにIDを貼り付け",  
    "ここにIDを貼り付け", 
    "ここにIDを貼り付け",  
    "ここにIDを貼り付け",  
]

# 初期ロール 
initial_role_id = "ここにIDを貼り付け"

# ロール付与処理
async def give_role(member, role_id):
    # 指定されたロールIDに対応するロールを取得
    role = member.guild.get_role(int(role_id))
    if role is not None:
        # メンバーにロールを追加
        try:
            await member.add_roles(role)
            print(f"ロール {role.name} を付与しました: {datetime.now(japan_tz)} to {member}")
        except discord.HTTPException as e:
            # ロール追加時のエラーハンドリング
            print(f"ロール {role.name} の付与中にエラーが発生しました: {e}")
    else:
        # ロールが見つからない場合のエラーメッセージ
        print(f"ロールID {role_id} が見つかりません。")

# 指定されたロールが付与されたことを監視
@bot.event
async def on_member_update(before, after):
    # 初期ロールが付与されたかどうかを確認
    initial_role = after.guild.get_role(int(initial_role_id))

    # 初期ロールが前の状態にはなく、後の状態にある場合
    if initial_role not in before.roles and initial_role in after.roles:
        # 初期ロールが付与されたら、最初のロール付与を開始
        await start_role_assignment(after, 0)
    else:
        # 新しいロールが付与されたら、次のロール付与を開始
        for index, role_id in enumerate(role_ids):
            role = after.guild.get_role(int(role_id))
            # 現在のメンバーが指定されたロールを持ち、次のロールが存在する場合
            if role in after.roles and index + 1 < len(role_ids):
                await start_role_assignment(after, index + 1)
                break

# ロールを順次付与する処理
async def start_role_assignment(member, role_index):
    # 全てのロールが付与済みの場合は終了
    if role_index >= len(role_ids):
        return

    # 付与時間を計算
    if role_index == 0:
        # 初期ロール付与時間を基準に次のロールまでの遅延を計算
        delay = timedelta(days=1, hours=18)
    else:
        # 前回のロール付与時間からの次の時間を計算
        roll_times = [
            timedelta(days=1, hours=12),         # 1日後の12時
            timedelta(days=2, hours=12),         
            timedelta(days=3, hours=12),        
            timedelta(days=4, hours=12),          
            timedelta(days=5, hours=12),         
        ]
        # 次のロールまでの遅延を設定
        delay = roll_times[role_index]

    # 次のロール付与時間まで待機
    try:
        await asyncio.sleep(delay.total_seconds())
    except asyncio.CancelledError:
        # タスクがキャンセルされた場合のハンドリング
        print(f"ロール付与タスクがキャンセルされました: {member}")
        return

    # 次のロールを付与
    await give_role(member, role_ids[role_index])

# ボットの起動
bot.run('YOUR_TOKEN_HERE')
