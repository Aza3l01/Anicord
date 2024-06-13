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
    guilds = await bot.rest.fetch_my_guilds()
    server_count = len(guilds)
    await bot.update_presence(
        activity=hikari.Activity(
            name=f"{server_count} servers! | /help",
            type=hikari.ActivityType.WATCHING,
        )
    )
    await topgg_client.post_guild_count(server_count)

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
        title="__Help__",
        description=(
            "**Core Commands:**\n"
            "**/core:** Overview of all core commands.\n\n"
            "**Role-play Reactions:**\n"
            "**/roleplay:** Overview of all role-play commands.\n\n"
            "**NSFW Role-play Reactions:**\n"
            "**/hroleplay:** Overview of all NSFW role-play commands.\n\n"
            "**Other NSFW Commands:**\n"
            "**/nsfw:** Overview of all NSFW commands like hentai memes and gifs.\n\n"
            "**Miscellaneous:**\n"
            "**/miscellaneous:** Overview of miscellaneous commands.\n\n"
            "NSFW commands are LOCKED from normal channels and are ONLY available in NSFW channels.."
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
        title="__**Core Commands**__",
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
async def anisearch(ctx: lightbulb.Context) -> None:
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
async def mangasearch(ctx: lightbulb.Context) -> None:
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
async def fetch_character_info(name, limit=5):
    async with aiohttp.ClientSession() as session:
        url = "https://api.jikan.moe/v4/characters"
        params = {
            "q": name,
            "limit": limit  # Increase the limit to fetch more characters
        }
        async with session.get(url, params=params) as response:
            if response.status != 200:
                print(f"Failed to fetch character data: HTTP {response.status}")
                return None
            return await response.json()

@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("name", "Character")
@lightbulb.command("character", "Look up a character.", auto_defer=True)
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
        title="__Role-play Reactions__",
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
#hroleplay
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("hroleplay", "Overview of all role-play commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def hroleplay(ctx):
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
        title="__NSFW Role-play Reactions__",
        description="NSFW commands are LOCKED from normal channels and are ONLY available in NSFW channels.",
        color=0x2B2D31
    )
    embed.add_field(
        name="Available",
        value=(
            "/fuck\n"
            "/blowjob\n"
            "/boobjob\n"
            "/handjob"
        ),
        inline=True
    )
    embed.add_field(
        name="Premium",
        value=(
            "/cum\n"
            "/ride\n"
            "/fingering\n"
            "/boobsuck"
        ),
        inline=True
    )
    embed.add_field(
        name="\u200B",
        value=("To use all premium commands for free, [vote](https://top.gg/bot/1003247499911376956/vote) on top.gg to gain access for the next 12 hours or become a [member](<https://buymeacoffee.com/azael/membership>).\n"),
        inline=False
    )
    embed.set_footer("Join the support server if you need help :)")
    await ctx.respond(embed=embed)

#free
#fuck
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("fuck", "Fuck someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def fuck(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gifs = [
        "https://cdn.discordapp.com/attachments/1243845586910838834/1250120862737240125/1.gif?ex=6669c947&is=666877c7&hm=fd3307a4a126b74c597ee8d4dfe58b284ec1b59857dc25f05de6d783340741e4&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1250120880542060645/2.gif?ex=6669c94c&is=666877cc&hm=4d7774510cf65e5a869bc46e935a5569692eacbe13e1722d4ca4a114894a66cd&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1250120892453748828/3.gif?ex=6669c94e&is=666877ce&hm=77a2ed76887f287eab6d5e4212e7c183dec96d938c8468b45cf19adc00dd5da8&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1250120907309973556/4.gif?ex=6669c952&is=666877d2&hm=eedb942c8509006f4fcac171d8dc23a39ecbfc4423fe71477290ae045a2ffd6f&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1250120923307315242/5.gif?ex=6669c956&is=666877d6&hm=693c8484d76fb965c9c9751ee05b3675b3b50cbb12c480e94eafc0fd486713cc&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1250120937551171749/6.gif?ex=6669c959&is=666877d9&hm=eb5817ae6e7b7472931b2fd526aecf404b6d66761fe47111a204fa43ae620aeb&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1250120947634016427/7.gif?ex=6669c95c&is=666877dc&hm=24f332a29e93229bff86d36c769c7a3a068377c9f76ec5ce944110268261b220&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1250120971382292550/8.gif?ex=6669c961&is=666877e1&hm=a65a02367c3097a4fad94071d9403655fe21d185a528101316f8f3248d98ced4&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1250120982052732948/9.gif?ex=6669c964&is=666877e4&hm=3fbb2330e44ba552057208c061b24c8ddfa62b3f83f6cc086c6aeb872c059792&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1250120993196740678/10.gif?ex=6669c966&is=666877e6&hm=b82555c39d60307f5984251e938bc64677118bfe012173cab13a8b4ad982d0c1&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1250121003619586099/11.gif?ex=6669c969&is=666877e9&hm=d95dbeb600c999b37c1aca2757fbf3a0e418f604d94dbe19fda6efd08d21f305&"
    ]

    random_gif = choice(gifs)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is fucking {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#blowjob
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("blowjob", "Receive a blowjob from someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def blowjob(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886126117290054/1250119594413264906/1.gif?ex=6669c819&is=66687699&hm=d81c7f71ea73d460e59b3f97c8722d731dea91ed6cc969d3a049d99d96c8419b&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1250119604781711392/2.gif?ex=6669c81b&is=6668769b&hm=12e754b68e21e945b3145aa2b926d4585de99c69eec60a772e8053d7ac7b0f43&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1250119614395056260/3.gif?ex=6669c81e&is=6668769e&hm=91e9d64563f17787073b75f02e20ae7f05f5dee6eed69a675ea37b0139a36ae1&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1250119638973677629/4.gif?ex=6669c824&is=666876a4&hm=35b7c440ee782f66c7eafbc421b87fe719050b392800975dc3c9b968bea2ef57&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1250119650839101615/5.gif?ex=6669c826&is=666876a6&hm=499477c92a0fef1ccaf2c801fd927028f1acc5b7f6d3fe6cb692ede0318e4c98&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1250119666148442193/6.gif?ex=6669c82a&is=666876aa&hm=e45adf9a9a83c20c30a9b2bad131e82451f5ac1a701965fbd6b61560677ab7d9&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1250119683525312653/7.gif?ex=6669c82e&is=666876ae&hm=e395e4696e2a480767d26d8b13c6f9659871575c6cc5d5fd245e72021c38c2c0&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1250119719403524197/8.gif?ex=6669c837&is=666876b7&hm=02c5ecc5aacfd992b099fdadced6469cb7a89012c5de13872cb353a0325795a6&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1250808015200718848/9.gif?ex=666c493d&is=666af7bd&hm=3f98b03484e23449a541d9a897e79c3ad8de46695344a128c26f42345327bd05&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1250809203744968767/10.gif?ex=666c4a59&is=666af8d9&hm=7627df0cefc7bcc9343c4455f7c2e8937093cc2ec139d9f9a855d80c5972a653&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is getting a blowjob from {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#boobjob
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("boobjob", "Receive a boobjob from someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def boobjob(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886173810856007/1250117099918065725/1.gif?ex=6669c5c6&is=66687446&hm=9c1fd984e2955e27cfa2e8f6d0fb1498b9db0742291add0cdabded13933d5502&",
        "https://cdn.discordapp.com/attachments/1243886173810856007/1250117113226592256/2.gif?ex=6669c5c9&is=66687449&hm=1a7d71e7b65b8ba973a2c51d8b11aaf7af194d607f617ba463bee005c833ed6e&",
        "https://cdn.discordapp.com/attachments/1243886173810856007/1250117133497663488/3.gif?ex=6669c5ce&is=6668744e&hm=5bf7831bc6c4feaf5d598ab39d7dc25e9e4425f1d5c556027f070a3d9f1456f1&",
        "https://cdn.discordapp.com/attachments/1243886173810856007/1250117144990056569/4.gif?ex=6669c5d1&is=66687451&hm=52888bb5e4dda9c309441833e79004098f055e5bc9586ffb8b72b0a490ddde0c&",
        "https://cdn.discordapp.com/attachments/1243886173810856007/1250117158088740948/5.gif?ex=6669c5d4&is=66687454&hm=4e921541413f6718f753fab5476a29c708644109eb517aad2a45a9f10ca28dc6&",
        "https://cdn.discordapp.com/attachments/1243886173810856007/1250117183430856796/6.gif?ex=6669c5da&is=6668745a&hm=5fe8c78e2bf0580750b37b1a3e3fcd9367ce5e1d79c6d274a0dbeb60e033fbda&",
        "https://cdn.discordapp.com/attachments/1243886173810856007/1250117202351358032/7.gif?ex=6669c5df&is=6668745f&hm=479b33018cb3acdfd6d28074282b95c88031a022aa85b9b11135a33d92013aa9&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is getting a boobjob from {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#handjob
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("handjob", "Receive a handjob from someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def handjob(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886203103875182/1250116179373195324/1.gif?ex=6669c4eb&is=6668736b&hm=4ec9375d1ddab0402945f8799e57e2f6f2a619e9500f90de17345b19eeb2c4f2&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1250116233253224591/2.gif?ex=6669c4f8&is=66687378&hm=73fcf71227ab33e72faf1c4cea4afd933f3d726026b5358e585e922540c8621e&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1250116251909361776/3.gif?ex=6669c4fc&is=6668737c&hm=40cd518bfee347b3e2a57b469e9c7d2109b55e30eea647bdc1f944c3cdfee0d8&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1250116262864879646/4.gif?ex=6669c4ff&is=6668737f&hm=f748dbc102c06b183925abebb566172f0f03c4aff91071138b8724182593897f&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1250116279784964096/5.gif?ex=6669c503&is=66687383&hm=c904f6b3e9299099ee74c76a42dc6c31de5ac0ce03175f12ddd8a78fb34a3107&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1250116284822196254/6.gif?ex=6669c504&is=66687384&hm=af98cbac347f716d189d07ccec0851c84d855f0546e07586abbb58196391cd0e&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1250808121597759488/7.gif?ex=666c4957&is=666af7d7&hm=8fec24bbf4a0d26ca070a03059c46e2dc74b3d0a86ade1c8806a79b159f35bba&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1250809697766739988/8.gif?ex=666c4ace&is=666af94e&hm=b04b3cbcfd751164b1ce93465d797b5cd9606630a0ff63ffff22460b781501e2&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is getting a handjob from {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#premium
#cum
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member", hikari.User)
@lightbulb.command("cum", "Cum on someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def sixtynine(ctx: lightbulb.Context) -> None:
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
    if str(ctx.author.id) not in prem_users:
        has_voted = await topgg_client.get_user_vote(ctx.author.id)
        if not has_voted:
            await ctx.respond("To use all premium commands for free, [vote](https://top.gg/bot/1003247499911376956/vote) on top.gg to gain access for the next 12 hours or become a [member](<https://buymeacoffee.com/azael/membership>).")
            await bot.rest.create_message(channel, f"Voting message was sent" + (f" in `{guild.name}`." if guild else "."))
            return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886267767459871/1250115545504944321/1.gif?ex=6669c454&is=666872d4&hm=bc039cbc1d0348cab34e3d6fdd84656dc67a2f35c32c95d35f0832c6bd4d01bd&",
        "https://cdn.discordapp.com/attachments/1243886267767459871/1250115556476981308/2.gif?ex=6669c456&is=666872d6&hm=f358e18204aa91285f39020473fcfb43171f03adf5dad843d26ee6c5acfcdd8d&",
        "https://cdn.discordapp.com/attachments/1243886267767459871/1250115569815126138/3.gif?ex=6669c459&is=666872d9&hm=0a3745ef214a8b6cf28a4904b79d490a8fe4b400c819d163cf07b9d97aae5cbe&",
        "https://cdn.discordapp.com/attachments/1243886267767459871/1250115580816789645/4.gif?ex=6669c45c&is=666872dc&hm=adad0ab0c9814dcebd49450e3ba3aa187d2a0dd9273bcfccea0098db0da15e31&",
        "https://cdn.discordapp.com/attachments/1243886267767459871/1250115598684262500/5.gif?ex=6669c460&is=666872e0&hm=17fdec70fbfab46cb42213feb7890728085d5398dc69365a0497d6c1df72bde1&",
        "https://cdn.discordapp.com/attachments/1243886267767459871/1250115610528972871/6.gif?ex=6669c463&is=666872e3&hm=26fb2e2d3efbfd1f6f9a4f8515730bc8748ea00361ba1da9231845b8998111f8&",
        "https://cdn.discordapp.com/attachments/1243886267767459871/1250362508229869598/7.gif?ex=666aaa54&is=666958d4&hm=d12b36865d67298d9e9ed7abe67ec5372e5e0c21b8246748305650d3ef7e7d71&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is cumming on {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)

#ride
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("ride", "Ride someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ride(ctx: lightbulb.Context) -> None:
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
    if str(ctx.author.id) not in prem_users:
        has_voted = await topgg_client.get_user_vote(ctx.author.id)
        if not has_voted:
            await ctx.respond("To use all premium commands for free, [vote](https://top.gg/bot/1003247499911376956/vote) on top.gg to gain access for the next 12 hours or become a [member](<https://buymeacoffee.com/azael/membership>).")
            await bot.rest.create_message(channel, f"Voting message was sent" + (f" in `{guild.name}`." if guild else "."))
            return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250114135606296606/1.gif?ex=6669c303&is=66687183&hm=e9a1a8ca6a6947dfde67350bde58c89dbcbccce18447da1cff4abe0367b1d28f&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250114171283181598/2.gif?ex=6669c30c&is=6668718c&hm=b06649af8a310af77b92e8d5d4c3c3ee43f10ccc7adaedeed57b560879af1f73&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250114182385369188/3.gif?ex=6669c30f&is=6668718f&hm=8df51e072bf96bbb4aaa3af5279a1827ace8d44ead9f84c97a39ec0e3b6f0706&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250114203944095754/4.gif?ex=6669c314&is=66687194&hm=f08aaf559b8cd7328217be73978fc8c12927008402e07e46ef4c215456456908&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250114216438927380/5.gif?ex=6669c317&is=66687197&hm=bee9dc9c2878869569abccfeea29d41e60ecbab9baa94dcf5ae269e489a17fcf&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250114231165124659/6.gif?ex=6669c31a&is=6668719a&hm=7a91c12b2e29de975119f55ee04f6348edc542a4379284df5276d024e44df455&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250114249444036668/7.gif?ex=6669c31f&is=6668719f&hm=79a26fd53e6980b376fbaf8c9005f8e151395e1e74bfb6168924c50765915f05&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250114270750834739/8.gif?ex=6669c324&is=666871a4&hm=8041e9f3722ce0851cdb50cfed06cc2cac8c9e52415992dc9dd83453fe25ff2d&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250114283832868954/9.gif?ex=6669c327&is=666871a7&hm=dccc76b721ea533ddb576f09e072547a562e5e91ec66dd6f4674f444407107ac&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250114300643639488/10.gif?ex=6669c32b&is=666871ab&hm=c3cac8aca935d930fa1f2b14afed1d49e8792eebc214611705ee7e58920309ad&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250808999436353678/11.gif?ex=666c4a28&is=666af8a8&hm=a87647170034b23a972829036bbcd4c568a5fa6b2afb4e89c87cd52ce36914f9&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250809005815889920/12.gif?ex=666c4a29&is=666af8a9&hm=10b27265014bab698f8cc638bea785b27186ebaad9fb0204b6ec1bdaf7de425e&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1250809673876246569/13.gif?ex=666c4ac9&is=666af949&hm=086b12c90db3434b957a8ed8613c1d2654745aba7159329cd25dcacc75b3f146&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is riding {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)

#fingering
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("fingering", "Finger someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def fingering(ctx: lightbulb.Context) -> None:
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
    if str(ctx.author.id) not in prem_users:
        has_voted = await topgg_client.get_user_vote(ctx.author.id)
        if not has_voted:
            await ctx.respond("To use all premium commands for free, [vote](https://top.gg/bot/1003247499911376956/vote) on top.gg to gain access for the next 12 hours or become a [member](<https://buymeacoffee.com/azael/membership>).")
            await bot.rest.create_message(channel, f"Voting message was sent" + (f" in `{guild.name}`." if guild else "."))
            return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886356879511602/1250112926296051832/1.gif?ex=6669c1e3&is=66687063&hm=5fcd42a3c8ced42869a0395784fc200ca4338ce3c8e1790d5d6b5c3d788e8fb3&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1250112941177569322/2.gif?ex=6669c1e7&is=66687067&hm=ae4879d990f23ef80906cbc81b7e12c5eba0c58fd28140a5694942bcac748442&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1250112962744684686/3.gif?ex=6669c1ec&is=6668706c&hm=9b39716f06f186988a2f2351ca3b95052a261a8c201354ec7e6910d3f276447d&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1250112977009512590/4.gif?ex=6669c1ef&is=6668706f&hm=2c954a4d3375d3b6477b05cd00923bd228af7fdd6bdf2adddb4048c374fb9027&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1250112991274340585/5.gif?ex=6669c1f3&is=66687073&hm=55394cc8925e32df5e502645d3de65659744fc72d6d9a8cdaa5b6a2df3cad56d&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1250113012799373312/6.gif?ex=6669c1f8&is=66687078&hm=89dc7d941975a8cbb3511428d27904afe10a7a8e45d2481872f8c68d3c2b3612&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1250113022374973440/7.gif?ex=6669c1fa&is=6668707a&hm=8791b203e17bdeae17fc40914c8aa91f81e077135af82ab1c86270c65527cb2d&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1250113051039109140/8.gif?ex=6669c201&is=66687081&hm=70e8ea1acd7e56f82197ca71837f206feb1755c96c7e5b3a314bb35f3f292d39&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1250808866950742026/9.gif?ex=666c4a08&is=666af888&hm=2ab42cbbc8197d4cf13969de0b8370bb172838844e619f33de90d858056e0c7e&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1250809521056780420/10.gif?ex=666c4aa4&is=666af924&hm=fa1b900b066310fcb9fd6e3b7006b7ac130860371a33c7080bfc425b0f5df6b5&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is fingering {ctx.options.user.mention}**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)

#boobsuck
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "Select a member.", hikari.User)
@lightbulb.command("boobsuck", "Suck on someone's boobs.")
@lightbulb.implements(lightbulb.SlashCommand)
async def boobsuck(ctx: lightbulb.Context) -> None:
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
    if str(ctx.author.id) not in prem_users:
        has_voted = await topgg_client.get_user_vote(ctx.author.id)
        if not has_voted:
            await ctx.respond("To use all premium commands for free, [vote](https://top.gg/bot/1003247499911376956/vote) on top.gg to gain access for the next 12 hours or become a [member](<https://buymeacoffee.com/azael/membership>).")
            await bot.rest.create_message(channel, f"Voting message was sent" + (f" in `{guild.name}`." if guild else "."))
            return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886396628930580/1250111991477964901/1.gif?ex=6669c104&is=66686f84&hm=4d91bdf261403aa154a6acba1c270628e720279a2fa75952fbeb979ddaa605cc&",
        "https://cdn.discordapp.com/attachments/1243886396628930580/1250112011308634203/2.gif?ex=6669c109&is=66686f89&hm=88585c16567df1b66c75ca033ae3c1269994b9ed8d381d97c9e303943b00e8eb&",
        "https://cdn.discordapp.com/attachments/1243886396628930580/1250112027201114235/3.gif?ex=6669c10d&is=66686f8d&hm=8bf8d840428c002bb53cd73dc690fda1fbf413a68bfce9a10ae6baa874075c49&",
        "https://cdn.discordapp.com/attachments/1243886396628930580/1250112041587314698/4.gif?ex=6669c110&is=66686f90&hm=e648f9b9230fbbeb64dad8c35a858ef11d8a582c49c10159b67da38504e3bb65&",
        "https://cdn.discordapp.com/attachments/1243886396628930580/1250112063351685182/5.gif?ex=6669c115&is=66686f95&hm=015bcbbbac2955abfa1a84e69286c4ca7fec912e3b6c57e98c0a24fe17eef20a&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is sucking {ctx.options.user.mention}'s boobs**",
        color=0x2B2D31
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)

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
        title="__NSFW Commands__",
        description=(
            "NSFW commands are LOCKED from normal channels and are ONLY available in NSFW channels.\n\n"
            "**/hmeme:** Get a hentai meme.\n"
            "**/hgif:** Get a hentai gif.\n"
            "**/himage:** Get a hentai image.\n\n"
            "To use all premium commands for free, [vote](https://top.gg/bot/1003247499911376956/vote) on top.gg to gain access for the next 12 hours or become a [member](<https://buymeacoffee.com/azael/membership>).\n"
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
    if str(ctx.author.id) not in prem_users:
        has_voted = await topgg_client.get_user_vote(ctx.author.id)
        if not has_voted:
            await ctx.respond("To use all premium commands for free, [vote](https://top.gg/bot/1003247499911376956/vote) on top.gg to gain access for the next 12 hours or become a [member](<https://buymeacoffee.com/azael/membership>).")
            await bot.rest.create_message(channel, f"Voting message was sent" + (f" in `{guild.name}`." if guild else "."))
            return
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
    if str(ctx.author.id) not in prem_users:
        has_voted = await topgg_client.get_user_vote(ctx.author.id)
        if not has_voted:
            await ctx.respond("To use all premium commands for free, [vote](https://top.gg/bot/1003247499911376956/vote) on top.gg to gain access for the next 12 hours or become a [member](<https://buymeacoffee.com/azael/membership>).")
            await bot.rest.create_message(channel, f"Voting message was sent" + (f" in `{guild.name}`." if guild else "."))
            return
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
    if str(ctx.author.id) not in prem_users:
        has_voted = await topgg_client.get_user_vote(ctx.author.id)
        if not has_voted:
            await ctx.respond("To use all premium commands for free, [vote](https://top.gg/bot/1003247499911376956/vote) on top.gg to gain access for the next 12 hours or become a [member](<https://buymeacoffee.com/azael/membership>).")
            await bot.rest.create_message(channel, f"Voting message was sent" + (f" in `{guild.name}`." if guild else "."))
            return
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
        title="__NSFW Commands__",
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
        title="__Miscellaneous__",
        description=(
            "**/invite:** Invite the bot to your server.\n"
            "**/vote:** Vote on top.gg.\n"
            "**/support:** Join the support server.\n"
            "**/donate:** Donate to support Anicord.\n"
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

#vote command
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("vote", "Vote on top.gg.")
@lightbulb.implements(lightbulb.SlashCommand)
async def vote(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
		title="Vote:",
		description="[Vote on top.gg, thank you!](https://top.gg/bot/1003247499911376956/vote)",
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

#donate command
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("donate", "Donate to support Anicord.")
@lightbulb.implements(lightbulb.SlashCommand)
async def donate(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="Donate:",
        description="[Donate to keep Anicord online, thank you!](https://buymeacoffee.com/azael)",
		color=0x2B2D31
	)
    await ctx.respond(embed=embed)

#more command
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("more", "More bots from me.")
@lightbulb.implements(lightbulb.SlashCommand)
async def more(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(channel, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="More:",
        description="[Check out more bots from me.](https://top.gg/user/67067136345571328)",
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
        await event.context.respond(f"`/{event.context.command.name}` is on cooldown. Retry in `{exception.retry_after:.0f}` seconds. ⏱️\nCommands are ratelimited to prevent spam abuse which could bring the bot down. To remove cool-downs, become a [member](<https://buymeacoffee.com/azael/membership>) for $3.")
    else:
        raise exception

#top.gg stop
@bot.listen(hikari.StoppedEvent)
async def on_stopping(event: hikari.StoppedEvent) -> None:
    await topgg_client.close()

bot.run()