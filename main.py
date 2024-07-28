import asyncio
import aiohttp
import hikari
import lightbulb
from mal import *
import praw
import jikanpy
from random import randint, choice
import os
from dotenv import load_dotenv

load_dotenv()
channel = os.getenv('CHANNEL_ID')
prem_users_string = os.getenv("PREM_USERS_LIST")
prem_users = prem_users_string.split(",")

jikan = jikanpy.Jikan()

bot = lightbulb.BotApp(token=os.getenv('BOT_TOKEN'))
animegan_api_key = os.getenv('ANIMEGAN_API_KEY')

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent="reddit app to pull posts to discord app by /u/licensed_",
    check_for_async=False
)

class TopGGClient:
    def __init__(self, bot, token):
        self.bot = bot
        self.token = token
        self.session = aiohttp.ClientSession()
    async def post_guild_count(self, count):
        url = f"https://top.gg/api/bots/{self.bot.get_me().id}/stats"
        headers = {
            "Authorization": self.token
        }
        payload = {
            "server_count": count
        }
        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                print(f"Failed to post guild count to Top.gg: {response.status}")
            else:
                print("Posted server count to Top.gg")
    async def get_user_vote(self, user_id):
        url = f"https://top.gg/api/bots/{self.bot.get_me().id}/check?userId={user_id}"
        headers = {
            "Authorization": self.token
        }
        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('voted') == 1
            return False
    async def close(self):
        await self.session.close()

topgg_token = os.getenv("TOPGG_TOKEN")
topgg_client = TopGGClient(bot, topgg_token)

#count update
@bot.listen(hikari.StartedEvent)
async def on_starting(event: hikari.StartedEvent) -> None:
    while True:
        guilds = await bot.rest.fetch_my_guilds()
        server_count = len(guilds)
        await bot.update_presence(
            activity=hikari.Activity(
                name=f"{server_count} servers! | /help",
                type=hikari.ActivityType.WATCHING,
            )
        )
        await topgg_client.post_guild_count(server_count)
        await asyncio.sleep(3600)

#join
@bot.listen(hikari.GuildJoinEvent)
async def on_guild_join(event):
    guild = event.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"Joined `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"Joined unknown server.")

#leave
@bot.listen(hikari.GuildLeaveEvent)
async def on_guild_leave(event):
    guild = event.old_guild
    if guild is not None:
        await bot.rest.create_message(channel, f"Left `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"Left unknown server.")

#help command
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("help", "Get help")
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="📚 Help 📚",
        description=(
            "**Core Commands:**\n"
            "**/core:** Overview of all core commands.\n\n"
            "**Role-play Reactions:**\n"
            "**/roleplay:** Overview of all role-play commands.\n\n"
            "**Other NSFW Commands:**\n"
            "**/nsfw:** Overview of all NSFW commands like hentai memes and gifs.\n\n"
            "**Miscellaneous:**\n"
            "**/miscellaneous:** Overview of miscellaneous commands.\n\n"
            "NSFW commands are LOCKED from normal channels and are ONLY available in NSFW channels."
        ),
        color=0x2B2D31
    )
    embed.set_footer("Join the support server if you need help :)")
    await ctx.respond(embed=embed)

#----------------------------------------------------------------------------------------
#core
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("core", "Overview of all core commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def core(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="🌸 Core Commands 🌸",
        description=(
            "**/anime:** Look up an anime.\n"
            "**/manga:** Look up a manga.\n"
            "**/character:** Look up a character.\n"
            "**/animeme:** View an anime meme.\n"
            "**/random:** Generate a random anime.\n"
        ),
        color=0x2B2D31
    )
    embed.set_footer("Join the support server if you need help :)")
    await ctx.respond(embed=embed)

#anime
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("name", "Anime")
@lightbulb.command("anime", "Look up an anime.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def anime(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    name = ctx.options.name
    search = AnimeSearch(name)
    anime_result = None
    if search.results[0] is not None:
        anime_result = search.results[0]
    elif len(search.results) > 1 and search.results[1] is not None:
        anime_result = search.results[1]
    else:
        await ctx.respond("No valid anime found.")
        return
    anime = Anime(anime_result.mal_id)
    embed = hikari.Embed(
        title=f"{anime.title_english or 'N/A'} | {anime.title_japanese or 'N/A'}",
        description=anime.synopsis or 'No synopsis available.',
        url=anime.url,
        color=0x2B2D31
    )
    embed.set_thumbnail(anime.image_url)
    if anime.premiered:
        embed.add_field(name="Premiered", value=anime.premiered, inline=True)
    if anime.status:
        embed.add_field(name="Status", value=anime.status, inline=True)
    if anime.type:
        embed.add_field(name="Type", value=anime.type, inline=True)
    if anime.score is not None:
        embed.add_field(name="Score", value=str(anime.score), inline=True)
    if anime.episodes is not None:
        embed.add_field(name="Episodes", value=str(anime.episodes), inline=True)
    if anime.broadcast:
        embed.add_field(name="Broadcast Time", value=anime.broadcast, inline=True)
    if anime.rank is not None:
        embed.add_field(name="Ranking", value=str(anime.rank), inline=True)
    if anime.popularity is not None:
        embed.add_field(name="Popularity", value=str(anime.popularity), inline=True)
    if anime.rating:
        embed.add_field(name="Rating", value=anime.rating, inline=True)
    embed.set_footer("Queries are served by an unofficial MAL API and Anicord has no control over the content.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    await ctx.respond(embed=embed)

#manga
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("name", "Manga")
@lightbulb.command("manga", "Look up a manga.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def manga(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    name = ctx.options.name
    search = MangaSearch(name)
    manga_result = None
    if search.results[0] is not None:
        manga_result = search.results[0]
    elif len(search.results) > 1 and search.results[1] is not None:
        manga_result = search.results[1]
    else:
        await ctx.respond("No valid manga found.")
        return
    manga = Manga(manga_result.mal_id)
    embed = hikari.Embed(
        title=f"{manga.title_english or 'N/A'} | {manga.title_japanese or 'N/A'}",
        description=manga.synopsis or 'No synopsis available.',
        url=manga.url,
        color=0x2B2D31
    )
    embed.set_thumbnail(manga.image_url)
    if manga.score is not None:
        embed.add_field(name="Score", value=str(manga.score), inline=True)
    if manga.rank is not None:
        embed.add_field(name="Ranking", value=str(manga.rank), inline=True)
    if manga.popularity is not None:
        embed.add_field(name="Popularity", value=str(manga.popularity), inline=True)
    if manga.status:
        embed.add_field(name="Status", value=manga.status, inline=True)
    if manga.chapters is not None:
        embed.add_field(name="Chapters", value=str(manga.chapters), inline=True)
    if manga.volumes is not None:
        embed.add_field(name="Volumes", value=str(manga.volumes), inline=True)
    embed.set_footer("Queries are served by an unofficial MAL API and Anicord has no control over the content.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    await ctx.respond(embed=embed)

#character
async def fetch_character_info(name, limit=25):
    url = "https://api.jikan.moe/v4/characters"
    params = {
        "q": name,
        "limit": limit
    }
    for attempt in range(3):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Failed to fetch character data: HTTP {response.status}")
                        return None
        except aiohttp.ClientConnectorError as e:
            print(f"Network error: {e}")
            await asyncio.sleep(1)
    return None

@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("name", "Character")
@lightbulb.command("character", "Look up a character. (May contain spoilers)", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def character(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    name = ctx.options.name.strip()
    character_data = await fetch_character_info(name)
    if not character_data or not character_data.get('data'):
        await ctx.respond("No valid character found.")
        return
    sorted_characters_by_popularity = sorted(character_data['data'], key=lambda x: x.get('favorites', 0), reverse=True)
    most_popular_character = sorted_characters_by_popularity[0]
    name_english = most_popular_character.get('name')
    name_japanese = most_popular_character.get('name_kanji')
    description = most_popular_character.get('about', 'No description available.')
    image_url = most_popular_character.get('images', {}).get('jpg', {}).get('image_url')
    mal_url = most_popular_character.get('url')
    details = []
    description_lines = description.split('\n')
    for line in description_lines:
        if ':' in line:
            details.append(line.strip())
    details_description = '\n'.join(details).strip()
    embed = hikari.Embed(
        title=f"{name_english} | {name_japanese}",
        url=mal_url,
        color=0x2B2D31
    )
    if image_url:
        embed.set_image(image_url)
    embed.description = details_description if details_description else "No specific details available."
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    await ctx.respond(embed=embed)

#animeme
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("animeme", "Get an anime meme.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def animeme(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    sub = reddit.subreddit("Animemes+goodanimemes")
    posts = [post for post in sub.hot(limit=60)]
    sfw_posts = [post for post in posts if not post.over_18]
    
    if not sfw_posts:
        await ctx.respond("Somehow all posts on reddit are NSFW right now, please try again later. 💀")
        return
    random_post = choice(sfw_posts)
    embed = hikari.Embed(
        title=random_post.title,
        description="",
        url="https://www.reddit.com" + random_post.permalink,
        color=0x2B2D31
    )
    embed.set_image(random_post.url)
    embed.set_footer("This content is served by the Reddit API and Anicord has no control over it.")
    await ctx.respond(embed=embed)

#random
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("random", "Generate a random anime.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def random(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    anime_id = randint(1, 5000)
    anime = Anime(anime_id)
    embed = hikari.Embed(
        title=f"{anime.title_english or 'N/A'} | {anime.title_japanese or 'N/A'}",
        description=anime.synopsis or 'No synopsis available.',
        url=anime.url,
        color=0x2B2D31
    )
    embed.set_thumbnail(anime.image_url)
    if anime.premiered:
        embed.add_field(name="Premiered", value=anime.premiered, inline=True)
    if anime.status:
        embed.add_field(name="Status", value=anime.status, inline=True)
    if anime.type:
        embed.add_field(name="Type", value=anime.type, inline=True)
    if anime.score is not None:
        embed.add_field(name="Score", value=str(anime.score), inline=True)
    if anime.episodes is not None:
        embed.add_field(name="Episodes", value=str(anime.episodes), inline=True)
    if anime.broadcast:
        embed.add_field(name="Broadcast Time", value=anime.broadcast, inline=True)
    if anime.rank is not None:
        embed.add_field(name="Ranking", value=str(anime.rank), inline=True)
    if anime.popularity is not None:
        embed.add_field(name="Popularity", value=str(anime.popularity), inline=True)
    if anime.rating:
        embed.add_field(name="Rating", value=anime.rating, inline=True)
    embed.set_footer("Queries are served by an unofficial MAL API and Anicord has no control over the content.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    await ctx.respond(embed=embed)

#----------------------------------------------------------------------------------------
#roleplay
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("roleplay", "Overview of all role-play commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def roleplay(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="🎴 Role-play Reactions 🎴",
        color=0x2B2D31
    )
    embed.add_field(
        name="Self Reactions",
        value=(
            "/happy\n"
            "/cry\n"
            "/beg\n"
            "/blush\n"
            "/facepalm\n"
            "/nosebleed\n"
            "/pout\n"
            "/run\n"
            "/shrug\n"
            "/smirk"
        ),
        inline=True
    )
    embed.add_field(
        name="Interactive Reactions",
        value=(
            "/wave\n"
            "/bite\n"
            "/bonk\n"
            "/hug\n"
            "/marry\n"
            "/kiss\n"
            "/lick\n"
            "/love\n"
            "/pat\n"
            "/slap"
        ),
        inline=True
    )
    embed.set_footer("Join the support server if you need help :)")
    await ctx.respond(embed=embed)

#Self
#happy
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("happy", "Emote as happy.")
@lightbulb.implements(lightbulb.SlashCommand)
async def happy(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"{ctx.author.mention} is happy.",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#cry
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("cry", "Emote as crying.")
@lightbulb.implements(lightbulb.SlashCommand)
async def cry(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/NMiID29TUvIAAAAC/hunter-x-hunter-gon-freecs.gif",
        "https://media1.tenor.com/m/0qj0aqZ0nucAAAAC/anya-spy-x-family-anime-anya-crying.gif",
        "https://media1.tenor.com/m/IHVd7sXB66YAAAAC/anime-cry-hinagiku.gif",
        "https://media1.tenor.com/m/y4wvESFaCAkAAAAC/%D9%85%D9%88%D8%AA-anime.gif",
        "https://media1.tenor.com/m/c1PMAiegtCkAAAAd/violet-evergarden-violet.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"{ctx.author.mention} is crying.",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#beg
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("beg", "Emote as begging.")
@lightbulb.implements(lightbulb.SlashCommand)
async def beg(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/rt-b5wrDLisAAAAC/bocchi-the-rock-bocchi.gif",
        "https://media1.tenor.com/m/o9V-PmmNGiwAAAAC/konosuba-aqua.gif",
        "https://media1.tenor.com/m/htjbZhCEDEoAAAAC/yui-cry.gif",
        "https://media1.tenor.com/m/c5NREl_bty0AAAAC/apologies-anime.gif",
        "https://media1.tenor.com/m/UL40uQSnBUsAAAAC/puppy-dog.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"{ctx.author.mention} is begging.",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    
#blush
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("blush", "Emote as blushing.")
@lightbulb.implements(lightbulb.SlashCommand)
async def blush(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/u1RaweQYumcAAAAC/anime-blushing.gif",
        "https://media1.tenor.com/m/yAM097mHhCQAAAAC/1.gif",
        "https://media1.tenor.com/m/CEkiOjpsylwAAAAd/kitagawa-kitagawa-marin.gif",
        "https://media1.tenor.com/m/FRunV08QBXwAAAAd/sumi-sakurasawa-rent-a-girlfriend.gif",
        "https://media1.tenor.com/m/sXv8LmKckugAAAAC/real.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"{ctx.author.mention} is blushing.",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#facepalm
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("facepalm", "Emote as facepalming.")
@lightbulb.implements(lightbulb.SlashCommand)
async def facepalm(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/ddev3tyfgAoAAAAC/haruhi-kyon.gif",
        "https://media1.tenor.com/m/Ktim6-Sh99oAAAAC/mitsuha.gif",
        "https://media1.tenor.com/m/X3QRuo_MqTEAAAAC/shikamaru-anime.gif"
        "https://media1.tenor.com/m/miK-GklQp2MAAAAC/facepalm-anime.gif",
        "https://media1.tenor.com/m/JTtGL2Sv-yoAAAAC/facepalm-oh-no.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"{ctx.author.mention} is facepalming.",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#nosebleed
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("nosebleed", "Emote as bleeding.")
@lightbulb.implements(lightbulb.SlashCommand)
async def nosebleed(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/Us2hPXlsqP8AAAAC/anime-girl.gif",
        "https://media1.tenor.com/m/Qy4yA2TMCmUAAAAC/nosebleed.gif",
        "https://media1.tenor.com/m/Q6W2cYwuNTIAAAAC/nose-bleed-anime-iruka-sensie.gif",
        "https://media1.tenor.com/m/xXK5Ug_0MJwAAAAC/anime-nosebleed.gif",
        "https://media1.tenor.com/m/2pOsYUAOZ5UAAAAC/zero-no-tsukaima-saito-hiraga.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"{ctx.author.mention} is bleeding from their nose.",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#pout
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("pout", "Emote as pouting.")
@lightbulb.implements(lightbulb.SlashCommand)
async def pout(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/yCR6JOoxS6wAAAAd/anime-angry.gif",
        "https://media1.tenor.com/m/03VCLMyKfL4AAAAC/pout-anime-pout.gif",
        "https://media1.tenor.com/m/KDxD-uZj08MAAAAC/anime-girl-annoyed.gif"
        "https://media1.tenor.com/m/tx3x8ANgbBwAAAAC/the-dreaming-boy-is-a-realist-yumemiru-danshi.gif",
        "https://media1.tenor.com/m/iNu8LXx2ECgAAAAC/senko-poute-hmph.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"{ctx.author.mention} is pouting.",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#run
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("run", "Emote as running.")
@lightbulb.implements(lightbulb.SlashCommand)
async def run(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/mUIXigPWPuYAAAAd/anime-anime-girl-running.gif",
        "https://media1.tenor.com/m/POl8wXpZBH0AAAAC/black-clover-charlotte.gif",
        "https://media1.tenor.com/m/XbfdY2Lx-zwAAAAC/zenitsu-running-away.gif",
        "https://media1.tenor.com/m/j6V8KlvWkzkAAAAC/one-punch-man-running.gif",
        "https://media1.tenor.com/m/fCb3HkXgHHUAAAAC/lyly-run.gif",
        "https://media1.tenor.com/m/MMA6_WvqS60AAAAC/escape-im-out.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"{ctx.author.mention} is running.",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#shrug
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("shrug", "Emote as shrugging.")
@lightbulb.implements(lightbulb.SlashCommand)
async def shrug(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/e1uPTuA2toIAAAAC/kana-shrug.gif",
        "https://media1.tenor.com/m/nlSDG33ptOoAAAAC/geto-suguru.gif",
        "https://media1.tenor.com/m/YdK9JDmImKUAAAAC/senyuu-anime.gif",
        "https://media1.tenor.com/m/WZd51JGLPKsAAAAd/shrug-anime-shrug.gif",
        "https://media1.tenor.com/m/0GOwPHgcUj0AAAAC/anime-shrug.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"{ctx.author.mention} is shrugging.",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#smirk
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("smirk", "Emote as smirking.")
@lightbulb.implements(lightbulb.SlashCommand)
async def smirk(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/Za14IOIKmioAAAAC/spy-x-family-anya-forger.gif",
        "https://media1.tenor.com/m/kyI_yjIwKE8AAAAC/anime-smirk-anime-perverted-smirk.gif",
        "https://media1.tenor.com/m/ZzsrPBR-Q1EAAAAC/anime-girl.gif",
        "https://media1.tenor.com/m/1UKtZSlQK68AAAAC/anime-santania.gif",
        "https://media1.tenor.com/m/uYewS1Vwk7cAAAAC/kazuma-sato-konosuba.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"{ctx.author.mention} is smirking.",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#Interactive
#wave
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", type=hikari.User)
@lightbulb.command("wave", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def wave(ctx: lightbulb.Context) -> None: 
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/nQOSTbcTKZcAAAAC/anime-waves-hi.gif",
        "https://media1.tenor.com/m/tzbVcnK8iGsAAAAC/keai-cute.gif",
        "https://media1.tenor.com/m/ILT5-vuNzB8AAAAC/anime-anime-wave-bye.gif",
        "https://media1.tenor.com/m/3u27loVq00AAAAAC/hand-wave.gif",
        "https://media1.tenor.com/m/H4xLf6epW-wAAAAC/anime-wave.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is waving at {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#bite
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("bite", "Bite someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def bite(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/5mVQ3ffWUTgAAAAC/anime-bite.gif",
        "https://media1.tenor.com/m/IKDf1NMrzsIAAAAC/anime-acchi-kocchi.gif",
        "https://media1.tenor.com/m/_AkeqheWU-4AAAAC/anime-bite.gif",
        "https://media1.tenor.com/m/ECCpi63jZlUAAAAC/anime-bite.gif",
        "https://media1.tenor.com/m/6HhJw-4zmQUAAAAC/anime-bite.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is biting {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#bonk
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("bonk", "Bonk someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def bonk(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/bkXZ1GhsTTsAAAAC/hitoribocchi-bocchi.gif",
        "https://media1.tenor.com/m/mXwNLMSQRN8AAAAC/yuru-yuri-chinatsu-yoshikawa.gif",
        "https://media1.tenor.com/m/DiGHoKx3x8kAAAAC/atonnic-bonk.gif",
        "https://media1.tenor.com/m/d1slOLImNHYAAAAC/anime-couple.gif",
        "https://media1.tenor.com/m/1NgForvfNAAAAAAC/no-more-brain-rikka-takanashi.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is bonking {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    
#hug
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("hug", "Hug someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def hug(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/kCZjTqCKiggAAAAC/hug.gif",
        "https://media1.tenor.com/m/J7eGDvGeP9IAAAAC/enage-kiss-anime-hug.gif",
        "https://media1.tenor.com/m/7oCaSR-q1kkAAAAC/alice-vt.gif",
        "https://media1.tenor.com/m/G_IvONY8EFgAAAAC/aharen-san-anime-hug.gif",
        "https://media1.tenor.com/m/FgLRE4gi5VoAAAAC/hugs-cute.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is hugging {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#marry
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("marry", "Marry someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def marry(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/R4EeoV4R-kUAAAAd/spy-x-family-loid-forger.gif",
        "https://media1.tenor.com/m/u7B_BCacat8AAAAC/wedding-ring-engaged.gif",
        "https://media1.tenor.com/m/UnSlrdcbV9kAAAAC/anime-ring.gif",
        "https://media1.tenor.com/m/kK8gAeHtSPMAAAAC/marry-me.gif",
        "https://media1.tenor.com/m/HieFdcgKYW4AAAAC/my-clueless-first-friend-anime-propose.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is marrying {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#kiss
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("kiss", "Kiss someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def kiss(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/PxN2rH6SJuUAAAAC/anime-kiss.gif",
        "https://media1.tenor.com/m/C96g4M5OPsYAAAAC/anime-couple.gif",
        "https://media1.tenor.com/m/g8AeFZoe7dsAAAAC/kiss-anime-kiss.gif",
        "https://media1.tenor.com/m/Daj-Pn82PagAAAAC/gif-kiss.gif",
        "https://media1.tenor.com/m/IAP6odUutZMAAAAC/kiss.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is kissing {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#lick
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("lick", "Lick someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def lick(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/Pb1JPfqXpAIAAAAC/lick-licky.gif",
        "https://media1.tenor.com/m/9CXrjvcyVa4AAAAC/rory-mercury.gif",
        "https://media1.tenor.com/m/jyv9sexi1fYAAAAC/anime-lick.gif",
        "https://media1.tenor.com/m/Go7wnhOWjSkAAAAC/anime-lick-face.gif",
        "https://media1.tenor.com/m/S5I9g4dPRn4AAAAC/omamori-himari-manga.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is licking {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#love
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("love", "Show your love to someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def love(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/fMMWtnu9g0oAAAAC/juvia-juvia-lockser.gif",
        "https://media1.tenor.com/m/PGXshKPAUh4AAAAC/my-dress-up-darling-anime-love.gif",
        "https://media1.tenor.com/m/IgM8Kbd3omAAAAAC/in-love-anime.gif",
        "https://media1.tenor.com/m/MS5qy7kP870AAAAC/anime-love.gif",
        "https://media1.tenor.com/m/XVnnV2Td8CAAAAAC/fangirling-fangirl.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is in love with {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#pat
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("pat", "Pat someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def pat(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/oGbO8vW_eqgAAAAC/spy-x-family-anya.gif",
        "https://media1.tenor.com/m/3PjRNS8paykAAAAC/pat-pat-head.gif",
        "https://media1.tenor.com/m/E6fMkQRZBdIAAAAC/kanna-kamui-pat.gif",
        "https://media1.tenor.com/m/Zm71HaIh7wwAAAAC/pat-pat.gif",
        "https://media1.tenor.com/m/DCMl9bvSDSwAAAAd/pat-head-gakuen-babysitters.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is patting {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#slap
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("slap", "Slap someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def slap(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/XiYuU9h44-AAAAAC/anime-slap-mad.gif",
        "https://media1.tenor.com/m/eU5H6GbVjrcAAAAC/slap-jjk.gif",
        "https://media1.tenor.com/m/cpWuWnOU64MAAAAC/bofetada.gif",
        "https://media1.tenor.com/m/sacuMyU4lkwAAAAC/anime-girl-anime.gif",
        "https://media1.tenor.com/m/Sv8LQZAoQmgAAAAC/chainsaw-man-csm.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is slapping {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#----------------------------------------------------------------------------------------
#nsfw
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("nsfw", "Overview of all role-play commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def nsfw(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="🔞 NSFW Commands 🔞",
        description=(
            "NSFW commands are LOCKED from normal channels and are ONLY available in NSFW channels.\n\n"
            "**/hmeme:** Get a hentai meme.\n"
            "**/hgif:** Get a hentai gif.\n"
            "**/himage:** Get a hentai image.\n\n"
            "To use NSFW premium commands for free, [vote](https://top.gg/bot/1003247499911376956/vote) on top.gg to gain access for the next 12 hours or become a [member](<https://ko-fi.com/azaelbots>).\n"
        ),
        color=0x2B2D31
    )
    embed.set_footer("Join the support server if you need help :)")
    await ctx.respond(embed=embed)

#hmeme
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("hmeme", "Get a hentai meme.")
@lightbulb.implements(lightbulb.SlashCommand)
async def hmeme(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    sub = reddit.subreddit("hentaimemes")
    posts = [post for post in sub.hot(limit=50)]
    random_post = choice(posts)
    
    embed = hikari.Embed(
        title=random_post.title,
        description="",
        url="https://www.reddit.com" + random_post.permalink,
        color=0x2B2D31
    )
    embed.set_image(random_post.url)
    embed.set_footer("This content is served by the Reddit API and Anicord has no control over it.")
    await ctx.respond(embed=embed)

#hgif
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("hgif", "Get a hentai gif.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def hgif(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    sub = reddit.subreddit("HENTAI_GIF")
    posts = [post for post in sub.hot(limit=50)]
    random_post = choice(posts)
    embed = hikari.Embed(
        title=random_post.title,
        description="",
        url="https://www.reddit.com" + random_post.permalink,
        color=0x2B2D31
    )
    embed.set_image(random_post.url)
    embed.set_footer("This content is served by the Reddit API and Anicord has no control over it.")
    await ctx.respond(embed=embed)

#himage
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("himage", "Get a hentai image.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def himage(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    sub = reddit.subreddit("hentai+nhentai+3DPorncraft")
    posts = list(sub.hot(limit=50))
    image_posts = [post for post in posts if post.url.endswith(('.jpg', '.jpeg', '.png'))]
    if not image_posts:
        await ctx.respond("No suitable images found in the subreddit.")
        return
    random_post = choice(image_posts)
    embed = hikari.Embed(
        title=random_post.title,
        description="",
        url=f"https://www.reddit.com{random_post.permalink}",
        color=0x2B2D31
    )
    embed.set_image(random_post.url)
    embed.set_footer("This content is served by the Reddit API and Anicord has no control over it.")
    await ctx.respond(embed=embed)

#----------------------------------------------------------------------------------------
#gimmick
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("gimmick", "Overview of all gimmick commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def gimmick(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="🎀 Gimmick Commands 🎀",
        description=(
            "**/howhorny:** Fine out how horny someone is.\n"
            "**/howgay:** Find out how gay someone is.\n"
            "**/ship:** Find out how compatible two users are.\n"
        ),
        color=0x2B2D31
    )
    embed.set_footer("Join the support server if you need help :)")
    await ctx.respond(embed=embed)

#howhorny
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("howhorny", "Find out how horny someone is.")
@lightbulb.implements(lightbulb.SlashCommand)
async def howhorny(ctx: lightbulb.Context) -> None:
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    
    horny_level = randint(0, 100)
    await ctx.respond(f"{ctx.options.user.mention} is **{horny_level}%** horny.")

#howgay
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("howgay", "Find out how gay someone is.")
@lightbulb.implements(lightbulb.SlashCommand)
async def howgay(ctx: lightbulb.Context) -> None:
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    
    horny_level = randint(0, 100)
    await ctx.respond(f"{ctx.options.user.mention} is **{horny_level}%** gay.")

#ship
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user2", "Select a member.", hikari.User)
@lightbulb.option("user1", "Select a member.", hikari.User)
@lightbulb.command("ship", "Find out how compatible two users are.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ship(ctx: lightbulb.Context) -> None:
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    compatibility_level = randint(0, 100)
    await ctx.respond(f"{ctx.options.user1.mention} and {ctx.options.user2.mention} are **{compatibility_level}%** compatible.")

#----------------------------------------------------------------------------------------
#Miscellaneous
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("miscellaneous", "Overview of all miscellaneous commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def miscellaneous(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="🛡️ Miscellaneous 🛡️",
        description=(
            "**/invite:** Invite the bot to your server.\n"
            "**/vote:** Vote on top.gg.\n"
            "**/support:** Join the support server.\n"
            "**/premium:** Learn more about the premium version of the bot.\n"
            "**/more:** More bots from me.\n"
            "**/privacy:** View our privacy policy."
        ),
        color=0x2B2D31
    )
    embed.set_footer("Join the support server if you need help :)")
    await ctx.respond(embed=embed)

#invite command
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("invite", "Invite the bot to your server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def invite(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="Invite:",
		description="[Invite the bot to your server.](https://discord.com/api/oauth2/authorize?client_id=1003247499911376956&permissions=414464723008&scope=bot%20applications.commands)",
		color=0x2B2D31
	)
    await ctx.respond(embed=embed)

#support command
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("support", "Join the support server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def support(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="Support:",
		description="[Join the support server.](https://discord.com/invite/x7MdgVFUwa)",
		color=0x2B2D31
	)
    await ctx.respond(embed=embed)

#privacy command
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("privacy", "Privacy policy statement.")
@lightbulb.implements(lightbulb.SlashCommand)
async def privacy(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
		title="Privacy Policy:",
		description="The personal information of any user, including the username or the commands used by a user, is not tracked by Anicord.\n\nThe user_id of premium members are stored to provide the user the with perks and is deleted once a user is no longer a member.\n\nJoin the [support server](https://discord.com/invite/x7MdgVFUwa) to request the deletion of your data.\n\n[Click to view the full privacy policy statement.](https://gist.github.com/Aza3l01/4374050bc9749c6588a6291629f08f39)",
		color=0x2B2D31
	)
    await ctx.respond(embed=embed)

#----------------------------------------------------------------------------------------
#error handling
@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond("Something went wrong, please try again. 😔")
        raise event.exception
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"`/{event.context.command.name}` is on cooldown. Retry in `{exception.retry_after:.0f}` seconds. ⏱️\nCommands are ratelimited to prevent spam abuse which could bring the bot down. To remove cool-downs, become a [member](<https://ko-fi.com/azaelbots>).")
    else:
        raise exception

#top.gg stop
@bot.listen(hikari.StoppedEvent)
async def on_stopping(event: hikari.StoppedEvent) -> None:
    await topgg_client.close()

bot.run()