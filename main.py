import aiohttp
import hikari
import lightbulb
from mal import *
import praw
import jikanpy
from random import randint, choice

jikan = jikanpy.Jikan()

bot = lightbulb.BotApp(
    token="MTAwMzI0NzQ5OTkxMTM3Njk1Ng.GbxSQg.HK-XlFjM7JGel8p7pwKZhwrwRJbfghgpReVJZQ"
)

reddit = praw.Reddit(
    client_id="ab7VFLYLR38dL3NwruCWhw",
    client_secret="VEYILiZE2EaH_sO8e8SyfSCfXzEJ7w",
    user_agent="reddit app to pull posts to discord app by /u/licensed_",
    check_for_async=False
)

#server count
@bot.listen()
async def on_starting(_: hikari.StartedEvent) -> None:
    await bot.update_presence(
        activity=hikari.Activity(
            name=f"{len([*await bot.rest.fetch_my_guilds()])} servers! | /help",
            type=hikari.ActivityType.WATCHING,
        )
    )

prem_users = ["364400063281102852"]

#help command
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("help", "Get help")
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="__**Help**__",
        description=(
            "**Core Commands:**\n"
            "**/core:** Overview of all core commands.\n\n"
            "**Role-play Reactions:**\n"
            "**/roleplay:** Overview of all role-play commands.\n\n"
            "**NSFW Role-play Reactions:**\n"
            "**/hroleplay:** Overview of NSFW all role-play commands.\n\n"
            "**Other NSFW Commands:**\n"
            "**/nsfw:** Overview of NSFW commands like hentai memes and gifs.\n\n"
            "**Miscellaneous:**\n"
            "**/misc:** Overview of miscellaneous commands.\n\n"
            "All NSFW commands are only accessible in NSFW channels."
        ),
        color=0x2f3136
    )
    embed.set_footer("Anicord is under development. Join the support server if you need help :)")
    await ctx.respond(embed=embed)
    await ctx.respond(
        embed=hikari.Embed(
            description=(
                "**Thank you!**\n"
                "If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\n"
                "To help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership)."
            ),
            color=0x2f3136
        )
    )

#----------------------------------------------------------------------------------------
#core
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("core", "Overview of all core commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def core(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="__**Core Commands**__",
        description=(
            "**/anime:** Look up an anime.\n"
            "**/manga:** Look up an manga.\n"
            "**/extended:** Choose between different search queries.\n"
            "**/character:** Look up a character.\n"
            "**/animeme:** View an anime meme.\n"
            "**/random:** Generate a random anime.\n"
        ),
        color=0x2f3136
    )
    embed.set_footer("Anicord is under development. Join the support server if you need help :)")
    await ctx.respond(embed=embed)

#anime
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("name", "Anime")
@lightbulb.command("anime", "Look up an anime.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def anisearch(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
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
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("name", "Manga")
@lightbulb.command("manga", "Look up a manga.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def mangasearch(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
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

#extended
@bot.command
@lightbulb.add_cooldown(length=1, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("extended", "Receive search queries for a more detailed experience.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def aniextended(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    await ctx.respond("/aniextended is currently unavailable but will be updated soon. Visit the [support server](https://discord.com/invite/CvpujuXmEf) for updates.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

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
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("name", "Character")
@lightbulb.command("character", "Look up a character.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def character(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
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
@lightbulb.command("animeme", "Get an anime meme.")
@lightbulb.implements(lightbulb.SlashCommand)
async def animeme(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
    )
    embed.set_image(random_post.url)
    embed.set_footer("This content is served by the Reddit API and Anicord has no control over it.")
    await ctx.respond(embed=embed)

#random
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("random", "Generate a random anime.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def random(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    anime_id = randint(1, 5000)

    anime = Anime(anime_id)

    embed = hikari.Embed(
        title=f"{anime.title_english or 'N/A'} | {anime.title_japanese or 'N/A'}",
        description=anime.synopsis or 'No synopsis available.',
        url=anime.url,
        color=0x2f3136
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
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("roleplay", "Overview of all role-play commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def roleplay(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

    embed = hikari.Embed(
        title="__**NSFW Role-play Reactions**__",
        color=0x2f3136
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
            "/cuddle\n"
            "/hug\n"
            "/kiss\n"
            "/lick\n"
            "/love\n"
            "/pat\n"
            "/slap"
        ),
        inline=True
    )
    embed.add_field(
        name="\u200B",
        value=(
            "More commands in development."
        ),
        inline=False
    )
    embed.set_footer("Anicord is under development. Join the support server if you need help :)")

    await ctx.respond(embed=embed)

#Self
#happy
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("happy", "Emote as happy.")
@lightbulb.implements(lightbulb.SlashCommand)
async def happy(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy. 😊",
        color=0x2f3136
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
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/NMiID29TUvIAAAAC/hunter-x-hunter-gon-freecs.gif",
        "https://media1.tenor.com/m/0qj0aqZ0nucAAAAC/anya-spy-x-family-anime-anya-crying.gif",
        "https://media1.tenor.com/m/IHVd7sXB66YAAAAC/anime-cry-hinagiku.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        title=f"{ctx.author.username} is crying. 😭",
        color=0x2f3136
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
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/rt-b5wrDLisAAAAC/bocchi-the-rock-bocchi.gif",
        "https://media1.tenor.com/m/o9V-PmmNGiwAAAAC/konosuba-aqua.gif",
        "https://media1.tenor.com/m/htjbZhCEDEoAAAAC/yui-cry.gif",
        "https://media1.tenor.com/m/c5NREl_bty0AAAAC/apologies-anime.gif",
        "https://media1.tenor.com/m/UL40uQSnBUsAAAAC/puppy-dog.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        title=f"{ctx.author.username} is begging you. 🥺",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    
#blush
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("blush", "Emote as crying.")
@lightbulb.implements(lightbulb.SlashCommand)
async def blush(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/NMiID29TUvIAAAAC/hunter-x-hunter-gon-freecs.gif",
        "https://media1.tenor.com/m/0qj0aqZ0nucAAAAC/anya-spy-x-family-anime-anya-crying.gif",
        "https://media1.tenor.com/m/IHVd7sXB66YAAAAC/anime-cry-hinagiku.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        title=f"{ctx.author.username} is blushing. 😳",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#facepalm
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("facepalm", "Emote as crying.")
@lightbulb.implements(lightbulb.SlashCommand)
async def facepalm(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/NMiID29TUvIAAAAC/hunter-x-hunter-gon-freecs.gif",
        "https://media1.tenor.com/m/0qj0aqZ0nucAAAAC/anya-spy-x-family-anime-anya-crying.gif",
        "https://media1.tenor.com/m/IHVd7sXB66YAAAAC/anime-cry-hinagiku.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        title=f"{ctx.author.username} is facepalming. 🤦",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#nosebleed
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("nosebleed", "Emote as crying.")
@lightbulb.implements(lightbulb.SlashCommand)
async def nosebleed(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/NMiID29TUvIAAAAC/hunter-x-hunter-gon-freecs.gif",
        "https://media1.tenor.com/m/0qj0aqZ0nucAAAAC/anya-spy-x-family-anime-anya-crying.gif",
        "https://media1.tenor.com/m/IHVd7sXB66YAAAAC/anime-cry-hinagiku.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        title=f"{ctx.author.username} is bleeding from their nose. 🩸",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#pout
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("pout", "Emote as crying.")
@lightbulb.implements(lightbulb.SlashCommand)
async def pout(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/NMiID29TUvIAAAAC/hunter-x-hunter-gon-freecs.gif",
        "https://media1.tenor.com/m/0qj0aqZ0nucAAAAC/anya-spy-x-family-anime-anya-crying.gif",
        "https://media1.tenor.com/m/IHVd7sXB66YAAAAC/anime-cry-hinagiku.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        title=f"{ctx.author.username} is pouting. 😾",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#run
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("run", "Emote as crying.")
@lightbulb.implements(lightbulb.SlashCommand)
async def run(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/NMiID29TUvIAAAAC/hunter-x-hunter-gon-freecs.gif",
        "https://media1.tenor.com/m/0qj0aqZ0nucAAAAC/anya-spy-x-family-anime-anya-crying.gif",
        "https://media1.tenor.com/m/IHVd7sXB66YAAAAC/anime-cry-hinagiku.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        title=f"{ctx.author.username} is running. 🏃",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#shrug
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("shrug", "Emote as crying.")
@lightbulb.implements(lightbulb.SlashCommand)
async def shrug(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/NMiID29TUvIAAAAC/hunter-x-hunter-gon-freecs.gif",
        "https://media1.tenor.com/m/0qj0aqZ0nucAAAAC/anya-spy-x-family-anime-anya-crying.gif",
        "https://media1.tenor.com/m/IHVd7sXB66YAAAAC/anime-cry-hinagiku.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        title=f"{ctx.author.username} is shrugging. 🤷",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#smirk
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("smirk", "Emote as crying.")
@lightbulb.implements(lightbulb.SlashCommand)
async def smirk(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/NMiID29TUvIAAAAC/hunter-x-hunter-gon-freecs.gif",
        "https://media1.tenor.com/m/0qj0aqZ0nucAAAAC/anya-spy-x-family-anime-anya-crying.gif",
        "https://media1.tenor.com/m/IHVd7sXB66YAAAAC/anime-cry-hinagiku.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        title=f"{ctx.author.username} is smirking. 😏",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#Interactive
#wave
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("wave", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def wave(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#bite
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("bite", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def bite(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#bonk
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("bonk", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def bonk(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    
#cuddle
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("cuddle", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def cuddle(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#hug
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("hug", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def hug(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#kiss
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("kiss", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def kiss(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#lick
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("lick", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def lick(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#love
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("love", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def love(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#pat
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("pat", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def pat(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#slap
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("slap", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def slap(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#----------------------------------------------------------------------------------------
#hroleplay
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("hroleplay", "Overview of all role-play commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def hroleplay(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

    embed = hikari.Embed(
        title="__**NSFW Role-play Reactions**__",
        color=0x2f3136
    )
    embed.add_field(
        name="Available",
        value=(
            "/fuck\n"
            "/anal\n"
            "/blowjob\n"
            "/boobjob\n"
            "/handjob"
        ),
        inline=True
    )
    embed.add_field(
        name="Premium",
        value=(
            "/69\n"
            "/cum\n"
            "/ride\n"
            "/fingering\n"
            "/boobsuck"
        ),
        inline=True
    )
    embed.add_field(
        name="\u200B",
        value=(
            "To use premium commands, become a [member](https://buymeacoffee.com/azael/membership).\n"
            "More commands in development."
        ),
        inline=False
    )
    embed.set_footer("Anicord is under development. Join the support server if you need help :)")

    await ctx.respond(embed=embed)

#free
#fuck
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("fuck", "Fuck someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def fuck(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#anal
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("anal", "Fuck someone in the ass.")
@lightbulb.implements(lightbulb.SlashCommand)
async def anal(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#blowjob
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("blowjob", "Receive a blowjob from someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def blowjob(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#boobjob
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("boobjob", "Receive a boobjob from someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def boobjob(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#handjob
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("handjob", "Receive a handjob from someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def handjob(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    
    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]
    
    random_gif = choice(gif)
    
    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    
    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"
    
    await ctx.respond(content=content, embed=embed)
    
    if any(str(ctx.author.id) == str(prem_user) for prem_user in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#premium
#69
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("69", "someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def happy(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    if str(ctx.author.id) not in prem_users:
        await ctx.respond("This is a premium command.")
        return

    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return

    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]

    random_gif = choice(gif)

    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)

    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"

    await ctx.respond(content=content, embed=embed)

#cum
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("cum", "someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def cum(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    if str(ctx.author.id) not in prem_users:
        await ctx.respond("This is a premium command.")
        return

    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return

    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]

    random_gif = choice(gif)

    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)

    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"

    await ctx.respond(content=content, embed=embed)

#ride
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("ride", "someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def ride(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    if str(ctx.author.id) not in prem_users:
        await ctx.respond("This is a premium command.")
        return

    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return

    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]

    random_gif = choice(gif)

    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)

    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"

    await ctx.respond(content=content, embed=embed)

#fingering
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("fingering", "someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def fingering(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    if str(ctx.author.id) not in prem_users:
        await ctx.respond("This is a premium command.")
        return

    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return

    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]

    random_gif = choice(gif)

    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)

    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"

    await ctx.respond(content=content, embed=embed)

#boobsuck
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User, required=False)
@lightbulb.command("boobsuck", "someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def boobsuck(ctx: lightbulb.Context, user: hikari.User = None) -> None:
    if str(ctx.author.id) not in prem_users:
        await ctx.respond("This is a premium command.")
        return

    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return

    gif = [
        "https://media1.tenor.com/m/ZQndYO4NwBcAAAAC/gojo-satoru.gif",
        "https://media1.tenor.com/m/uXIogZmtfiYAAAAC/haru-yoshida-tonari-no-kaibutsu-kun.gif",
        "https://media1.tenor.com/m/myCsjxxbtXAAAAAC/anime-happy.gif",
        "https://media1.tenor.com/m/3fAZZncIHDQAAAAC/smile-anime.gif",
        "https://media1.tenor.com/m/ssO9d-jnRYIAAAAd/chika-fujiwara-spinning.gif",
        "https://media1.tenor.com/m/4fjOL2wLihcAAAAC/yum-anime.gif"
    ]

    random_gif = choice(gif)

    embed = hikari.Embed(
        title=f"{ctx.author.username} is happy!",
        color=0x2f3136
    )
    embed.set_image(random_gif)

    if user:
        content = f"{user.mention}, {ctx.author.username} is happy!"
    else:
        content = f"{ctx.author.username} is happy!"

    await ctx.respond(content=content, embed=embed)

#----------------------------------------------------------------------------------------
#nsfw
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("nsfw", "Overview of all role-play commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def nsfw(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="__**NSFW Commands**__",
        description=(
            "**/hmeme:** Get a hentai meme.\n"
            "**/hgif:** Get a hentai gif.\n"
            "**/hgif3d:** Get a 3D hentai gif.\n"
            "**/himage:** Get a hentai image.\n"
            "**/himage3d:** Get a 3D hentai image.\n"
            "More Commands In Development."
        ),
        color=0x2f3136
    )
    embed.set_footer("Anicord is under development. Join the support server if you need help :)")
    await ctx.respond(embed=embed)

#hmeme
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("hmeme", "Get a hentai meme.")
@lightbulb.implements(lightbulb.SlashCommand)
async def hmeme(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
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
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
    )
    embed.set_image(random_post.url)
    embed.set_footer("This content is served by the Reddit API and Anicord has no control over it.")
    await ctx.respond(embed=embed)

#hgif3d
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("hgif3dtesting", "Get a 3D hentai gif.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def hgif3dtesting(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return

    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    
    sub = await reddit.subreddit("3DPorncraft+3DHentai")
    posts = [post for post in await sub.hot(limit=50) if post.url.endswith('.gif')]
    
    if not posts:
        await ctx.respond("No GIFs found.")
        return

    random_post = choice(posts)
    
    embed = hikari.Embed(
        title=random_post.title,
        description="",
        url="https://www.reddit.com" + random_post.permalink,
        color=0x2f3136
    )
    embed.set_image(random_post.url)
    embed.set_footer("This content is served by the Reddit API and Anicord has no control over it.")
    await ctx.respond(embed=embed)

#himage
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("himage", "Get an image.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def himage(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    # Check if the channel is NSFW
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return

    # Reset cooldown for premium users
    if any(str(ctx.author.id) == user_id for user_id in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    
    # Fetch subreddit posts
    sub = reddit.subreddit("hentai+nhentai")
    posts = list(sub.hot(limit=50))

    # Filter image posts
    image_posts = [post for post in posts if post.url.endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_posts:
        await ctx.respond("No suitable images found in the subreddit.")
        return
    
    # Select a random post from the filtered image posts
    random_post = choice(image_posts)
    
    # Create an embed with the post details
    embed = hikari.Embed(
        title=random_post.title,
        description="",
        url=f"https://www.reddit.com{random_post.permalink}",
        color=0x2f3136
    )
    embed.set_image(random_post.url)
    embed.set_footer("This content is served by the Reddit API and Anicord has no control over it.")
    
    await ctx.respond(embed=embed)

#himage3d
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("himage3dtesting", "Get an image.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def himage3dtesting(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
    # Check if the channel is NSFW
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return

    # Reset cooldown for premium users
    if any(str(ctx.author.id) == user_id for user_id in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    
    # Fetch subreddit posts
    sub = reddit.subreddit("3DPorncraft")
    posts = list(sub.hot(limit=50))

    # Filter image posts
    image_posts = [post for post in posts if post.url.endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_posts:
        await ctx.respond("No suitable images found in the subreddit.")
        return
    
    # Select a random post from the filtered image posts
    random_post = choice(image_posts)
    
    # Create an embed with the post details
    embed = hikari.Embed(
        title=random_post.title,
        description="",
        url=f"https://www.reddit.com{random_post.permalink}",
        color=0x2f3136
    )
    embed.set_image(random_post.url)
    embed.set_footer("This content is served by the Reddit API and Anicord has no control over it.")
    
    await ctx.respond(embed=embed)

#----------------------------------------------------------------------------------------
#misc
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("misc", "Overview of all role-play commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def misc(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="__**Miscellaneous**__",
        description=(
            "**/invite:** Get the bot's invite link.\n"
            "**/vote:** Get the link to vote at top.gg.\n"
            "**/support:** Invite to join the support server.\n"
            "**/donate:** Donate to support Anicord.\n"
            "**/more:** Check out more bots from me.\n"
            "**/privacy:** View our privacy policy."
        ),
        color=0x2f3136
    )
    embed.set_footer("Anicord is under development. Join the support server if you need help :)")
    await ctx.respond(embed=embed)

#invite command
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("invite", "Get the bot's invite link.")
@lightbulb.implements(lightbulb.SlashCommand)
async def invite(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="Invite:",
		description="Get the bot's invite link [here](https://discord.com/api/oauth2/authorize?client_id=1003247499911376956&permissions=414464723008&scope=bot%20applications.commands).",
		color=0x2f3136
	)
    await ctx.respond(embed=embed)
    embed = embed = hikari.Embed(
		title = '',
			description = '**Thank you!** \n If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\nIf you want to help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership).',
			color = 0x2f3136
		)
    await ctx.respond(embed=embed)

#vote command
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("vote", "Get the link to vote at top.gg.")
@lightbulb.implements(lightbulb.SlashCommand)
async def vote(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
		title="Vote:",
		description="Click [here](https://top.gg/bot/1003247499911376956/vote) to vote on top.gg. Thank you!",
		color=0x2f3136
    )
    await ctx.respond(embed=embed)
    embed = embed = hikari.Embed(
		title = '',
			description = '**Thank you!** \n If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\nIf you want to help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership).',
			color = 0x2f3136
		)
    await ctx.respond(embed=embed)

#support command
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("support", "Invite to join the support server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def support(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="Support:",
		description="Click [here](https://discord.com/invite/CvpujuXmEf) to join the support server.",
		color=0x2f3136
	)
    await ctx.respond(embed=embed)
    embed = embed = hikari.Embed(
		title = '',
			description = '**Thank you!** \n If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\nIf you want to help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership).',
			color = 0x2f3136
		)
    await ctx.respond(embed=embed)

#donate command
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("donate", "Donate to support Anicord.")
@lightbulb.implements(lightbulb.SlashCommand)
async def donate(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="Donate:",
        description="[Buy me a coffee](https://www.buymeacoffee.com/azael) to keep Anicord alive. Thank you! :)",
		color=0x2f3136
	)
    await ctx.respond(embed=embed)
    embed = embed = hikari.Embed(
		title = '',
			description = '**Thank you!** \n If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\nIf you want to help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership).',
			color = 0x2f3136
		)
    await ctx.respond(embed=embed)

#more command
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("more", "Check out more bots from me.")
@lightbulb.implements(lightbulb.SlashCommand)
async def more(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
        title="More:",
        description="Click [here](https://top.gg/user/67067136345571328) to check out more bots from me.",
        color=0x2f3136
    )
    await ctx.respond(embed=embed)
    embed = embed = hikari.Embed(
		title = '',
			description = '**Thank you!** \n If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\nIf you want to help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership).',
			color = 0x2f3136
		)
    await ctx.respond(embed=embed)

#privacy command
@bot.command
@lightbulb.command("privacy", "View our privacy policy statement.")
@lightbulb.implements(lightbulb.SlashCommand)
async def privacy(ctx):
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    embed = hikari.Embed(
		title="",
		description="**Privacy Policy:** \n The personal information of any user, including the message content it replies to, is not tracked by Anicord.",
		color=0x2f3136
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
        await event.context.respond(f"`/{event.context.command.name}` is on cooldown. Retry in `{exception.retry_after:.0f}` seconds. ⏱️ \n API commands are ratelimited to prevent spam abuse which could bring the bot down. \n To avoid cooldowns, become a member at https://www.buymeacoffee.com/azael.")
    else:
        raise exception

bot.run()