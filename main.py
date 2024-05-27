import aiohttp
import hikari
import lightbulb
from mal import *
import praw
import jikanpy
from random import randint, choice
import asyncio

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
    async def close(self):
        await self.session.close()

topgg_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwMDMyNDc0OTk5MTEzNzY5NTYiLCJib3QiOnRydWUsImlhdCI6MTY1OTYwMjk3Mn0.-TxpE4GNZSkgBPYQHQJ9vCD20_3lN_D-jImpcVIz928"
topgg_client = TopGGClient(bot, topgg_token)

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

prem_users = ["364400063281102852", "982029598600613949"]

#join
@bot.listen(hikari.GuildJoinEvent)
async def on_guild_join(event):
    guild = event.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"Joined `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"Joined unknown server.")
    guild = event.guild
    general_channel = None
    for channel in guild.get_channels().values():
        if isinstance(channel, hikari.TextableChannel) and "general" in channel.name.lower():
            general_channel = channel
            break
    if general_channel is None:
        for channel in guild.get_channels().values():
            if isinstance(channel, hikari.TextableChannel):
                general_channel = channel
                break
    if general_channel is not None:
        embed = hikari.Embed(
            title="Thank you for inviting me here! 🫶",
            description=(
                "**Please use the commands below to get an overview of all the commands.**\n\n"
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
                "All NSFW commands are only accessible in NSFW channels.\n"
                "This message will be deleted in 5 minutes."
            ),
            color=0x2f3136
        )
        embed.set_footer("Anicord is under development. Join the support server if you need help :)")
        message = await general_channel.send(embed=embed)
        await asyncio.sleep(300)
        await message.delete()

#help command
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("help", "Get help")
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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

#----------------------------------------------------------------------------------------
#core
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("core", "Overview of all core commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def core(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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

#anime
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("name", "Anime")
@lightbulb.command("anime", "Look up an anime.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def anisearch(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
@lightbulb.add_cooldown(length=30, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("name", "Anime")
@lightbulb.command("extended", "Receive search queries to choose for a more detailed experience.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def extended(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if str(ctx.author.id) in prem_users:
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
        name = ctx.options.name
        search = AnimeSearch(name)
        if len(search.results) < 4:
            await ctx.respond("Not enough search results found.", flags=hikari.MessageFlag.EPHEMERAL)
            return
        anime_options = [Anime(result.mal_id) for result in search.results[:4]]
        components = []
        action_row = hikari.ActionRowBuilder()
        for i in range(4):
            button = hikari.ButtonBuilder(style=hikari.ButtonStyle.PRIMARY, custom_id=f"button_{i}", emoji=f"{i+1}️⃣")
            action_row.add_component(button)
        components.append(action_row.build())
        embed = hikari.Embed(
            title="Choose a show:",
            description="\n".join([f"{i+1}️⃣ {anime.title}" for i, anime in enumerate(anime_options)]),
            color=0x2f3136
        )
        await ctx.respond(embed=embed, component=components)
        @bot.listen(hikari.InteractionCreateEvent)
        async def on_button_click(event: hikari.InteractionCreateEvent) -> None:
            if event.interaction.user.id != ctx.author.id:
                return  # Ensure only the command user can interact
            if event.interaction.component_type != hikari.ComponentType.BUTTON:
                return
            button_id = event.interaction.custom_id
            if button_id.startswith("button_"):
                index = int(button_id.split("_")[1])
                anime = anime_options[index]
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
                await event.interaction.create_initial_response(hikari.ResponseType.MESSAGE_UPDATE, embed=embed, component=None)

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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
@lightbulb.command("animeme", "Get an anime meme.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def animeme(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

    embed = hikari.Embed(
        title="__**Role-play Reactions**__",
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
    embed.add_field(
        name="\u200B",
        value=(
            "More commands in development."
        ),
        inline=False
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

#Self
#happy
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("happy", "Emote as happy.")
@lightbulb.implements(lightbulb.SlashCommand)
async def happy(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
        description=f"{ctx.author.mention} is begging.",
        color=0x2f3136
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
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
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
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
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
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
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
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
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
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    gif = [
        "https://media1.tenor.com/m/mUIXigPWPuYAAAAd/anime-anime-girl-running.gif",
        "https://media1.tenor.com/m/POl8wXpZBH0AAAAC/black-clover-charlotte.gif",
        "https://media1.tenor.com/m/XbfdY2Lx-zwAAAAC/zenitsu-running-away.gif",
        "https://media1.tenor.com/m/j6V8KlvWkzkAAAAC/one-punch-man-running.gif",
        "https://media1.tenor.com/m/fCb3HkXgHHUAAAAC/lyly-run.gif"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"{ctx.author.mention} is running.",
        color=0x2f3136
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
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
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
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
@lightbulb.option("user", "user to tag", type=hikari.User)
@lightbulb.command("wave", "Wave at someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def wave(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#bite
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "user to tag", hikari.User)
@lightbulb.command("bite", "Bite someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def bite(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#bonk
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "user to tag", hikari.User)
@lightbulb.command("bonk", "Bonk someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def bonk(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
    
#hug
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "user to tag", hikari.User)
@lightbulb.command("hug", "Hug someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def hug(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#marry
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "user to tag", hikari.User)
@lightbulb.command("marry", "Marry someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def marry(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
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
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#kiss
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "user to tag", hikari.User)
@lightbulb.command("kiss", "Kiss someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def kiss(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
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
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#lick
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "user to tag", hikari.User)
@lightbulb.command("lick", "Lick someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def lick(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    
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
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#love
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "user to tag", hikari.User)
@lightbulb.command("love", "Show your love to someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def love(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#pat
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "user to tag", hikari.User)
@lightbulb.command("pat", "Pat someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def pat(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#slap
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "user to tag", hikari.User)
@lightbulb.command("slap", "Slap someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def slap(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#----------------------------------------------------------------------------------------
#hroleplay
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("hroleplay", "Overview of all role-play commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def hroleplay(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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

#free
#fuck
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "user to tag", hikari.User)
@lightbulb.command("fuck", "Fuck someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def fuck(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243845586910838834/1244389195997384724/fucking2.gif?ex=6654ef3f&is=66539dbf&hm=a51ca33ce38b389cbbd25705f9032c2e3373525ac8c0d742a5e02a3ab1578141&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1244389219372371998/fucking3.gif?ex=6654ef45&is=66539dc5&hm=5f2c0602a6f23078e059342e8bcce5f84f5b3f5b9e45bc7bf2b94ae3afe0637a&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1244389242474463393/fucking4.gif?ex=6654ef4b&is=66539dcb&hm=03478effce2b7101cc83fc198042e03803ca22d5458ae8c5dd67e22de7730918&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1244389267464126534/fucking5.gif?ex=6654ef50&is=66539dd0&hm=406e2124f83a9eaa4a07a45a84a3744d1ac00b564fa8b08fe1f707da5a0b274f&",
        "https://cdn.discordapp.com/attachments/1243845586910838834/1244389280655212604/fucking6.gif?ex=6654ef54&is=66539dd4&hm=4cfbb483e7f2ccb4227e3b7e1367f4027dd521741b9341aadab4c93f91d43ba1&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is fucking {ctx.options.user.mention}**",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#anal
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User)
@lightbulb.command("anal", "Fuck someone in the ass.")
@lightbulb.implements(lightbulb.SlashCommand)
async def anal(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886094278459422/1244588808150847539/anal1.gif?ex=6655a927&is=665457a7&hm=d12d086a95f8d548f4843af7505c8cd32980f15095e6ff9df16c6c8b573c2b49&",
        "https://cdn.discordapp.com/attachments/1243886094278459422/1244588827696168970/anal2.gif?ex=6655a92b&is=665457ab&hm=a95d536ff7275de6c6ab7fb78c4131ffbdb59fd7a95e4102374106ce37afeb4e&",
        "https://cdn.discordapp.com/attachments/1243886094278459422/1244588836520988712/anal3.gif?ex=6655a92d&is=665457ad&hm=dcbaa85738f1f0f81dd56b26bc196803048a7b4e9ec27890693d8ceb1feda903&",
        "https://cdn.discordapp.com/attachments/1243886094278459422/1244588853902184469/anal4.gif?ex=6655a932&is=665457b2&hm=1640d7d4729c9aed4a279a8573278f8a1340d831179f75c1c1a092c883240081&",
        "https://cdn.discordapp.com/attachments/1243886094278459422/1244588864044273664/anal5.gif?ex=6655a934&is=665457b4&hm=0f5303f58c5f095f319aca42fa9e6ea22d719294d018b1d673fcd07b30ee34d7&",
        "https://cdn.discordapp.com/attachments/1243886094278459422/1244588878912815164/anal6.gif?ex=6655a938&is=665457b8&hm=e16e3d25a875ba396d48745ebe2eddc5e53f36624937219765a1f75459e3df07&",
        "https://cdn.discordapp.com/attachments/1243886094278459422/1244588890325520414/anal7.gif?ex=6655a93a&is=665457ba&hm=a07189af810bf9833d6b9a7d3b443a6c85d6bc07a8cbaaaf3b78b4a1e37a5a50&",
        "https://cdn.discordapp.com/attachments/1243886094278459422/1244588900614279290/anal8.gif?ex=6655a93d&is=665457bd&hm=8dd32362da8c621222ccd35f6542255e417f2ac96eee8fc02d3d4732e86d522c&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is fucking {ctx.options.user.mention} in the ass**",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#blowjob
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User)
@lightbulb.command("blowjob", "Receive a blowjob from someone.")
@lightbulb.implements(lightbulb.SlashCommand)
async def blowjob(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886126117290054/1244591246287310909/1.gif?ex=6655ab6c&is=665459ec&hm=693c621746fea96df63d88fff0562e2433cefad28aac18c0ec9c230439374237&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1244591257641160704/2.gif?ex=6655ab6f&is=665459ef&hm=358b2fe0aacf4381a0ab591287dd31ccc3459678499d302af2f8268e642e59f4&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1244591279749468210/3.gif?ex=6655ab74&is=665459f4&hm=a0db81aeb5c028e01b67db89b29fb96c9a2ce1030cd7066ced66a9c0e59e644d&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1244591295008210965/4.gif?ex=6655ab78&is=665459f8&hm=0f844958a133552682fec05c170c7e97a3f1b9faebaa672a73b60f70f021c2e2&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1244591311777042554/5.gif?ex=6655ab7c&is=665459fc&hm=f21370c0c28e1c6b2b4330f148206ad2c6a31207b173a4517f6dab881a234614&",
        "https://cdn.discordapp.com/attachments/1243886126117290054/1244591323567095859/6.gif?ex=6655ab7e&is=665459fe&hm=7f68c4d7192257df87dd86cda647b145ac36969e419074a2e6df65703d5dbdbc&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is getting a blowjob from {ctx.options.user.mention}**",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#boobjob
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User)
@lightbulb.command("boobjob", "Receive a boobjob from someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def boobjob(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886173810856007/1244593956545630279/1.gif?ex=6655adf2&is=66545c72&hm=da398791b74e52bf5fbd2aaae1254b11a202b5fb4d9d4a40cd42b15e98dde35b&",
        "https://cdn.discordapp.com/attachments/1243886173810856007/1244593967174127646/2.gif?ex=6655adf5&is=66545c75&hm=9ad8cb0e38da72be5011a530933d6e9fd7fe78d94e2ee56013c0a3e8e0c14a06&",
        "https://cdn.discordapp.com/attachments/1243886173810856007/1244594265422565416/3.gif?ex=6655ae3c&is=66545cbc&hm=10ec90489275fb0cc964fd438ab68251833f8cb13297ec39e365156cfbb0f5ee&",
        "https://cdn.discordapp.com/attachments/1243886173810856007/1244593999923249203/4.gif?ex=6655adfd&is=66545c7d&hm=08f1a0a1b6b290d8a4cc8235f2b00d3f85ee96a0d6e279202c688c39c022eb3f&",
        "https://cdn.discordapp.com/attachments/1243886173810856007/1244594018856468500/5.gif?ex=6655ae01&is=66545c81&hm=ad0ed2af1433413b36f5cce75a58ad4fac6afa837dbe444e47e0c9b61eefc7ff&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is getting a boobjob from {ctx.options.user.mention}**",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#handjob
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User)
@lightbulb.command("handjob", "Receive a handjob from someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def handjob(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886203103875182/1244595894100168704/1.gif?ex=6655afc0&is=66545e40&hm=02450e97aa38728448fec8d71aead0a76ca2623a0018eb595aa4245e632dd20b&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1244595938874363935/2.gif?ex=6655afcb&is=66545e4b&hm=6e4d0fa3bc1e953615ba312764dc5af462576378a751c2ec2ec7b19785325cc7&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1244596020923469924/3.gif?ex=6655afde&is=66545e5e&hm=2c36b17fd1b4841e0929bca4a8327a3ac34af9cd98f71e0b79581c6223def0e4&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1244596065102073856/4.gif?ex=6655afe9&is=66545e69&hm=e2bd01ad925a702797c8c21508a3ee83b26958702fbab72bc6032637be8df7e6&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1244596086018932748/5.gif?ex=6655afee&is=66545e6e&hm=3527de2655e8118bd0d8581904a5a111ce8b608b21b33b2c32691536e07a82c7&",
        "https://cdn.discordapp.com/attachments/1243886203103875182/1244596066368753684/6.gif?ex=6655afe9&is=66545e69&hm=e11c2b1eb2f8e2b6e6ba1b34237a0e12694bf9c71e171d6cf61d6b949f806325&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is getting a handjob from {ctx.options.user.mention}**",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

#premium
#69
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User)
@lightbulb.command("69", "someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def sixtynine(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if str(ctx.author.id) not in prem_users:
        await ctx.respond("This is a premium command. To use this command, become a [member](https://buymeacoffee.com/azael/membership). Memberships help keep the bot online.")
        return
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886239955025932/1244708659481804891/3.gif?ex=665618c5&is=6654c745&hm=2ed041d2f3b691880b72e09f85ed6dd95611e388575e73b7c8b0c0592fe4df68&",
        "https://cdn.discordapp.com/attachments/1243886239955025932/1244708680650199170/1.gif?ex=665618cb&is=6654c74b&hm=a4abe30ae028f41c0e12846af3ad50a321c30da4264ccade6c3a79ba79653344&",
        "https://cdn.discordapp.com/attachments/1243886239955025932/1244708690439835761/2.gif?ex=665618cd&is=6654c74d&hm=c7eef81d264c0b1b79f9c1d01299f7b4340378e3f49727d5431c14970636b262&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is doing 69 with {ctx.options.user.mention}**",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)

#cum
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User)
@lightbulb.command("cum", "someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def sixtynine(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if str(ctx.author.id) not in prem_users:
        await ctx.respond("This is a premium command. To use this command, become a [member](https://buymeacoffee.com/azael/membership). Memberships help keep the bot online.")
        return
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886267767459871/1244710926880473119/1.gif?ex=66561ae2&is=6654c962&hm=36e77cfac89bcf2672476b8ce0710d6b2121439cdc6dcddcf0c32f45540ba2bb&",
        "https://cdn.discordapp.com/attachments/1243886267767459871/1244710926880473119/1.gif?ex=66561ae2&is=6654c962&hm=36e77cfac89bcf2672476b8ce0710d6b2121439cdc6dcddcf0c32f45540ba2bb&",
        "https://cdn.discordapp.com/attachments/1243886267767459871/1244710926880473119/1.gif?ex=66561ae2&is=6654c962&hm=36e77cfac89bcf2672476b8ce0710d6b2121439cdc6dcddcf0c32f45540ba2bb&",
        "https://cdn.discordapp.com/attachments/1243886267767459871/1244710926880473119/1.gif?ex=66561ae2&is=6654c962&hm=36e77cfac89bcf2672476b8ce0710d6b2121439cdc6dcddcf0c32f45540ba2bb&",
        "https://cdn.discordapp.com/attachments/1243886267767459871/1244710926880473119/1.gif?ex=66561ae2&is=6654c962&hm=36e77cfac89bcf2672476b8ce0710d6b2121439cdc6dcddcf0c32f45540ba2bb&",
        "https://cdn.discordapp.com/attachments/1243886267767459871/1244710926880473119/1.gif?ex=66561ae2&is=6654c962&hm=36e77cfac89bcf2672476b8ce0710d6b2121439cdc6dcddcf0c32f45540ba2bb&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is cumming on {ctx.options.user.mention}**",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)

#ride
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User)
@lightbulb.command("ride", "someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def sixtynine(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if str(ctx.author.id) not in prem_users:
        await ctx.respond("This is a premium command. To use this command, become a [member](https://buymeacoffee.com/azael/membership). Memberships help keep the bot online.")
        return
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886309068767354/1244713699269283870/1.gif?ex=66561d77&is=6654cbf7&hm=4b119beb0a5f504c8db3f23d3818721105af8fd325036fc29ce8c933f7f133fb&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1244713776272375849/2.gif?ex=66561d89&is=6654cc09&hm=dfba715860c550517735022236ff17aac410247ad121fc112e6647be72b3dc84&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1244713762880098344/3.gif?ex=66561d86&is=6654cc06&hm=459fe081b9beb4c6a6fdd007b46a946d0bc1f65cac04bcc9fec4e963441ac0dd&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1244713759696490536/4.gif?ex=66561d85&is=6654cc05&hm=04e565991b6562837846998dda3201670e950ef5bb1001304c622a1862ab92c1&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1244713789589553252/5.gif?ex=66561d8d&is=6654cc0d&hm=b458de2e69aed45e887834bcc8abbed84b6d0ed6db3026ad9b108f31c8d1c06b&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1244713810443632680/6.gif?ex=66561d92&is=6654cc12&hm=f220b177f0d270fe321998ea4dcc8719aace5b4661c0da54379ff7c9f8c26ca5&",
        "https://cdn.discordapp.com/attachments/1243886309068767354/1244713788004106330/7.gif?ex=66561d8c&is=6654cc0c&hm=038a5ea64ee47f25565acef0325f7bbe7cb0bb98729567af999aea7c6b35f264&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is riding {ctx.options.user.mention}**",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)

#fingering
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User)
@lightbulb.command("fingering", "someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def sixtynine(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if str(ctx.author.id) not in prem_users:
        await ctx.respond("This is a premium command. To use this command, become a [member](https://buymeacoffee.com/azael/membership). Memberships help keep the bot online.")
        return
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886356879511602/1244716343274639360/1.gif?ex=66561fed&is=6654ce6d&hm=b55d1c3d927f835ca0aead2fc6dad7d9f8d43be7abfd4f12577a56d184fa396b&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1244716354309984257/2.gif?ex=66561ff0&is=6654ce70&hm=4b670ef46fdb70548a105ff37d07cdee399dc59cb1ad4799d268be0e88a04e0d&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1244716369577119764/3.gif?ex=66561ff4&is=6654ce74&hm=70b3df09a635fe0723b0088b1eac5eaf487bd66edf65d66d64d911c4e6023d27&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1244716380515995698/4.gif?ex=66561ff6&is=6654ce76&hm=eeb4293b9c2e927dc1ec4a732695f04772d78121b5d614ad05ed1a8fcb91ef10&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1244716422211309721/7.gif?ex=66562000&is=6654ce80&hm=1af15cf1f3dbf271f54772017a74bdd87272463b38d2a32f2ed6d923597d4c8c&",
        "https://cdn.discordapp.com/attachments/1243886356879511602/1244716428892835850/8.gif?ex=66562002&is=6654ce82&hm=fd43eb8bccbd29db36ae78a5a88937a248ed8e9a6cd800cdd99a1167dc9a76ed&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is fingering {ctx.options.user.mention}**",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)

#boobsuck
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("user", "The user to tag", hikari.User)
@lightbulb.command("boobsuck", "someone")
@lightbulb.implements(lightbulb.SlashCommand)
async def sixtynine(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if str(ctx.author.id) not in prem_users:
        await ctx.respond("This is a premium command. To use this command, become a [member](https://buymeacoffee.com/azael/membership). Memberships help keep the bot online.")
        return
    if not ctx.get_channel().is_nsfw:
        await ctx.respond("This command can only be used in NSFW channels.")
        return
    gif = [
        "https://cdn.discordapp.com/attachments/1243886396628930580/1244719521432866912/1.gif?ex=665622e3&is=6654d163&hm=03259432b4f33cbff7ad2de7cf07251540f5cf52b297b434547a02425f8a82e3&",
        "https://cdn.discordapp.com/attachments/1243886396628930580/1244719554022604800/3.gif?ex=665622eb&is=6654d16b&hm=5f498d6c12cf852aca6816bba0fa56abaa2c99a234b35e0bea451d158cbb7dce&",
        "https://cdn.discordapp.com/attachments/1243886396628930580/1244719560662450317/4.gif?ex=665622ed&is=6654d16d&hm=a5270fcb4de4becf4ed6628d75c813a82b01a3f908a6121a000f617e6947a3d0&",
        "https://cdn.discordapp.com/attachments/1243886396628930580/1244719576558731436/2.gif?ex=665622f0&is=6654d170&hm=6259913cb2b0ee834b75b17e12f339b53dd953f6119012f5ee569caa6680108c&",
        "https://cdn.discordapp.com/attachments/1243886396628930580/1244719613758148628/5.gif?ex=665622f9&is=6654d179&hm=88718abf81e55e047610e512876fdb4769069bd18e698e0961b02d8da4ed9ad5&"
    ]
    random_gif = choice(gif)
    embed = hikari.Embed(
        description=f"**{ctx.author.mention} is sucking {ctx.options.user.mention}'s boobs**",
        color=0x2f3136
    )
    embed.set_image(random_gif)
    await ctx.respond(embed=embed)

#----------------------------------------------------------------------------------------
#nsfw
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("nsfw", "Overview of all role-play commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def nsfw(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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

#hmeme
@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("hmeme", "Get a hentai meme.")
@lightbulb.implements(lightbulb.SlashCommand)
async def hmeme(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
@lightbulb.command("hgif3d", "Get a 3D hentai gif.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def hgif3d(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
@lightbulb.command("himage3d", "Get an image.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def himage3d(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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

#invite command
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command("invite", "Get the bot's invite link.")
@lightbulb.implements(lightbulb.SlashCommand)
async def invite(ctx):
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
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
    guild = ctx.get_guild()
    if guild is not None:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used in `{guild.name}`.")
    else:
        await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
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
        await event.context.respond(f"`/{event.context.command.name}` is on cooldown. Retry in `{exception.retry_after:.0f}` seconds. ⏱️ \n API commands are ratelimited to prevent spam abuse which could bring the bot down. \n To avoid cooldowns, become a [member](https://buymeacoffee.com/azael/membership).")
    else:
        raise exception

@bot.listen(hikari.StoppedEvent)
async def on_stopping(event: hikari.StoppedEvent) -> None:
    await topgg_client.close()

bot.run()