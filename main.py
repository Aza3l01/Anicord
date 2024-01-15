import hikari
import lightbulb
from mal import *
import praw
import random

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

prem_users = [
    "364400063281102852"
]

#anisearch
@bot.command
@lightbulb.add_cooldown(length = 15, uses = 1, bucket = lightbulb.UserBucket)
@lightbulb.option("name", "Anime")
@lightbulb.command("anisearch", "Look up an anime.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def anisearch(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
        name = ctx.options.name
        search = AnimeSearch(name)
        anime = Anime(search.results[0].mal_id)
        embed = hikari.Embed(
            title=f"{anime.title_english} | {anime.title_japanese}",
            description=anime.synopsis,
            url=anime.url,
            color=0x2f3136
        )
        embed.set_thumbnail(anime.image_url)
        embed.add_field(name="Premiered", value=anime.premiered, inline=True)
        embed.add_field(name="Status", value=anime.status, inline=True)
        embed.add_field(name="Type", value=anime.type, inline=True)
        embed.add_field(name="Score", value=anime.score, inline=True)
        embed.add_field(name="Episodes", value=anime.episodes, inline=True)
        embed.add_field(name="Broadcast Time", value=anime.broadcast, inline=True)
        embed.add_field(name="Ranking", value=anime.rank, inline=True)
        embed.add_field(name="Popularity", value=anime.popularity, inline=True)
        embed.add_field(name="Rating", value=anime.rating, inline=True)
        embed.set_footer("Queries are served by an unoffical MAL API and Anicord has no control over the content.")
        await ctx.respond(embed=embed)
    else:
        name = ctx.options.name
        search = AnimeSearch(name)
        anime = Anime(search.results[0].mal_id)
        embed = hikari.Embed(
            title=f"{anime.title_english} | {anime.title_japanese}",
            description=anime.synopsis,
            url=anime.url,
            color=0x2f3136
        )
        embed.set_thumbnail(anime.image_url)
        embed.add_field(name="Premiered", value=anime.premiered, inline=True)
        embed.add_field(name="Status", value=anime.status, inline=True)
        embed.add_field(name="Type", value=anime.type, inline=True)
        embed.add_field(name="Score", value=anime.score, inline=True)
        embed.add_field(name="Episodes", value=anime.episodes, inline=True)
        embed.add_field(name="Broadcast Time", value=anime.broadcast, inline=True)
        embed.add_field(name="Ranking", value=anime.rank, inline=True)
        embed.add_field(name="Popularity", value=anime.popularity, inline=True)
        embed.add_field(name="Rating", value=anime.rating, inline=True)
        embed.set_footer("Queries are served by an unoffical MAL API and Anicord has no control over the content.")
        await ctx.respond(embed=embed)

#manga
@bot.command
@lightbulb.add_cooldown(length = 15, uses = 1, bucket = lightbulb.UserBucket)
@lightbulb.option("name", "Manga")
@lightbulb.command("mangasearch", "Look up a manga.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def mangasearch(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
        name = ctx.options.name
        search = MangaSearch(name)
        manga = Manga(search.results[0].mal_id)
        embed = hikari.Embed(
            title=f"{manga.title_english} | {manga.title_japanese}",
            description=manga.synopsis,
            url=manga.url,
            color=0x2f3136
        )
        embed.set_thumbnail(manga.image_url)
        embed.add_field(name="Score", value=manga.score, inline=True)
        embed.add_field(name="Ranking", value=manga.rank, inline=True)
        embed.add_field(name="Popularity", value=manga.popularity, inline=True)
        embed.add_field(name="Status", value=manga.status, inline=True)
        embed.add_field(name="Chapters", value=manga.chapters, inline=True)
        embed.add_field(name="Volumes", value=manga.volumes, inline=True)
        embed.set_footer("Queries are served by an unoffical MAL API and Anicord has no control over the content.")
        await ctx.respond(embed=embed)
    else:
        name = ctx.options.name
        search = MangaSearch(name)
        manga = Manga(search.results[0].mal_id)
        embed = hikari.Embed(
            title=f"{manga.title_english} | {manga.title_japanese}",
            description=manga.synopsis,
            url=manga.url,
            color=0x2f3136
        )
        embed.set_thumbnail(manga.image_url)
        embed.add_field(name="Score", value=manga.score, inline=True)
        embed.add_field(name="Ranking", value=manga.rank, inline=True)
        embed.add_field(name="Popularity", value=manga.popularity, inline=True)
        embed.add_field(name="Status", value=manga.status, inline=True)
        embed.add_field(name="Chapters", value=manga.chapters, inline=True)
        embed.add_field(name="Volumes", value=manga.volumes, inline=True)
        embed.set_footer("Queries are served by an unoffical MAL API and Anicord has no control over the content.")
        await ctx.respond(embed=embed)

#animeme
@bot.command
@lightbulb.add_cooldown(length = 15, uses = 1, bucket = lightbulb.UserBucket)
@lightbulb.command("animeme", "Get an anime meme.")
@lightbulb.implements(lightbulb.SlashCommand)
async def animeme(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
        sub = reddit.subreddit("Animemes+goodanimemes")
        posts = [post for post in sub.hot(limit=20)]
        random_post_number = random.randint(0, 20)
        random_post = posts[random_post_number]
        embed = hikari.Embed(
            title=random_post.title,
            description="",
            url="https://www.reddit.com" + random_post.permalink,
            color=0x2f3136
        )
        embed.set_image(random_post.url)
        embed.set_footer("This content is served by the Reddit API and Anicord has no control over it.")
        await ctx.respond(embed=embed)
    else:
        sub = reddit.subreddit("Animemes+goodanimemes")
        posts = [post for post in sub.hot(limit=20)]
        random_post_number = random.randint(0, 20)
        random_post = posts[random_post_number]
        embed = hikari.Embed(
            title=random_post.title,
            description="",
            url="https://www.reddit.com" + random_post.permalink,
            color=0x2f3136
        )
        embed.set_image(random_post.url)
        embed.set_footer("This content is served by the Reddit API and Anicord has no control over it.")
        await ctx.respond(embed=embed)

#aniextended
@bot.command
@lightbulb.add_cooldown(length = 30, uses = 1, bucket = lightbulb.UserBucket)
@lightbulb.option("name", "Anime")
@lightbulb.command("aniextended", "Receive search queries to choose for a more detailed experience.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def aniextended(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)
        components = ctx.bot.rest.build_action_row()
        button_one = components.add_button(1, "one")
        button_two = components.add_button(1, "two")
        button_three = components.add_button(1, "three")
        button_four = components.add_button(1, "four")
        button_one.set_emoji("1️⃣")
        button_two.set_emoji("2️⃣")
        button_three.set_emoji("3️⃣")
        button_four.set_emoji("4️⃣")
        button_one.add_to_container()
        button_two.add_to_container()
        button_three.add_to_container()
        button_four.add_to_container()
        name = ctx.options.name
        search = AnimeSearch(name)
        global anime0
        anime0 = Anime(search.results[0].mal_id)
        global anime1
        anime1 = Anime(search.results[1].mal_id)
        global anime2
        anime2 = Anime(search.results[2].mal_id)
        global anime3
        anime3 = Anime(search.results[3].mal_id)
        embed = hikari.Embed(
            title="Choose a show:",
            description=f"1️⃣ {anime0.title} \n 2️⃣ {anime1.title} \n 3️⃣ {anime2.title} \n 4️⃣ {anime3.title}",
            color=0x2f3136
        )
        await ctx.respond(embed=embed, component=components)
    else:
        components = ctx.bot.rest.build_action_row()
        button_one = components.add_button(1, "one")
        button_two = components.add_button(1, "two")
        button_three = components.add_button(1, "three")
        button_four = components.add_button(1, "four")
        button_one.set_emoji("1️⃣")
        button_two.set_emoji("2️⃣")
        button_three.set_emoji("3️⃣")
        button_four.set_emoji("4️⃣")
        button_one.add_to_container()
        button_two.add_to_container()
        button_three.add_to_container()
        button_four.add_to_container()
        name = ctx.options.name
        search = AnimeSearch(name)
        global anime00
        anime0 = Anime(search.results[0].mal_id)
        global anime11
        anime1 = Anime(search.results[1].mal_id)
        global anime22
        anime2 = Anime(search.results[2].mal_id)
        global anime33
        anime3 = Anime(search.results[3].mal_id)
        embed = hikari.Embed(
            title="Choose a show:",
            description=f"1️⃣ {anime0.title} \n 2️⃣ {anime1.title} \n 3️⃣ {anime2.title} \n 4️⃣ {anime3.title}",
            color=0x2f3136
        )
        await ctx.respond(embed=embed, component=components)

@bot.listen(hikari.InteractionCreateEvent)
async def on_component_interaction(event: hikari.InteractionCreateEvent) -> None:
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return

    if event.interaction.custom_id == "one":
        embed0 = hikari.Embed(
            title=f"{anime0.title_english} | {anime0.title_japanese}",
            description=anime0.synopsis,
            url=anime0.url,
            color=0x2f3136
        )
        embed0.set_thumbnail(anime0.image_url)
        embed0.add_field(name="Premiered", value=anime0.premiered, inline=True)
        embed0.add_field(name="Status", value=anime0.status, inline=True)
        embed0.add_field(name="Type", value=anime0.type, inline=True)
        embed0.add_field(name="Score", value=anime0.score, inline=True)
        embed0.add_field(name="Episodes", value=anime0.episodes, inline=True)
        embed0.add_field(name="Broadcast Time", value=anime0.broadcast, inline=True)
        embed0.add_field(name="Ranking", value=anime0.rank, inline=True)
        embed0.add_field(name="Popularity", value=anime0.popularity, inline=True)
        embed0.add_field(name="Rating", value=anime0.rating, inline=True)
        embed0.set_footer("Queries are served by an unoffical MAL API and Anicord has no control over the content.")
        await event.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed=embed0,
            )

    if event.interaction.custom_id == "two":
        embed1 = hikari.Embed(
            title=f"{anime1.title_english} | {anime1.title_japanese}",
            description=anime1.synopsis,
            url=anime1.url,
            color=0x2f3136
        )
        embed1.set_thumbnail(anime1.image_url)
        embed1.add_field(name="Premiered", value=anime1.premiered, inline=True)
        embed1.add_field(name="Status", value=anime1.status, inline=True)
        embed1.add_field(name="Type", value=anime1.type, inline=True)
        embed1.add_field(name="Score", value=anime1.score, inline=True)
        embed1.add_field(name="Episodes", value=anime1.episodes, inline=True)
        embed1.add_field(name="Broadcast Time", value=anime1.broadcast, inline=True)
        embed1.add_field(name="Ranking", value=anime1.rank, inline=True)
        embed1.add_field(name="Popularity", value=anime1.popularity, inline=True)
        embed1.add_field(name="Rating", value=anime1.rating, inline=True)
        embed1.set_footer("Queries are served by an unoffical MAL API and Anicord has no control over the content.")
        await event.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed=embed1,    
            )

    if event.interaction.custom_id == "three":
        embed2 = hikari.Embed(
            title=f"{anime2.title_english} | {anime2.title_japanese}",
            description=anime2.synopsis,
            url=anime2.url,
            color=0x2f3136
        )
        embed2.set_thumbnail(anime2.image_url)
        embed2.add_field(name="Premiered", value=anime2.premiered, inline=True)
        embed2.add_field(name="Status", value=anime2.status, inline=True)
        embed2.add_field(name="Type", value=anime2.type, inline=True)
        embed2.add_field(name="Score", value=anime2.score, inline=True)
        embed2.add_field(name="Episodes", value=anime2.episodes, inline=True)
        embed2.add_field(name="Broadcast Time", value=anime2.broadcast, inline=True)
        embed2.add_field(name="Ranking", value=anime2.rank, inline=True)
        embed2.add_field(name="Popularity", value=anime2.popularity, inline=True)
        embed2.add_field(name="Rating", value=anime2.rating, inline=True)
        embed2.set_footer("Queries are served by an unoffical MAL API and Anicord has no control over the content.")
        await event.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed=embed2,    
            )

    if event.interaction.custom_id == "four":
        embed3 = hikari.Embed(
            title=f"{anime3.title_english} | {anime3.title_japanese}",
            description=anime3.synopsis,
            url=anime3.url,
            color=0x2f3136
        )
        embed3.set_thumbnail(anime3.image_url)
        embed3.add_field(name="Premiered", value=anime3.premiered, inline=True)
        embed3.add_field(name="Status", value=anime3.status, inline=True)
        embed3.add_field(name="Type", value=anime3.type, inline=True)
        embed3.add_field(name="Score", value=anime3.score, inline=True)
        embed3.add_field(name="Episodes", value=anime3.episodes, inline=True)
        embed3.add_field(name="Broadcast Time", value=anime3.broadcast, inline=True)
        embed3.add_field(name="Ranking", value=anime3.rank, inline=True)
        embed3.add_field(name="Popularity", value=anime3.popularity, inline=True)
        embed3.add_field(name="Rating", value=anime3.rating, inline=True)
        embed3.set_footer("Queries are served by an unoffical MAL API and Anicord has no control over the content.")
        await event.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                embed=embed3,    
            )

#help command
@bot.command
@lightbulb.command("help", "Get help")
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    embed = hikari.Embed(
		title="__**Commands**__",
		description="**__Main:__** \n **/anisearch:** Look up an anime. \n **/mangasearch:** Look up a manga. \n **/animeme:** Get an anime meme. \n \n **__Extended Search:__** \n **/aniextended:** Receive search queries to choose for a more detailed experience. \n \n **__Misc:__** \n **/invite:** Get the bot's invite link. \n **/vote:** Get the link to vote at top.gg. \n **/support:** Invite to join the support server. \n **/donate:** Donate to support Anicord. \n **/more:** Check out more bots from me.",
		color = 0x2f3136
	)
    embed.set_footer("Anicord is very new and under development. Feel free to join the support server, if you're having trouble using the bot :)")
    await ctx.respond(embed=embed)

#invite command
@bot.command
@lightbulb.command("invite", "Get the bot's invite link.")
@lightbulb.implements(lightbulb.SlashCommand)
async def invite(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    embed = hikari.Embed(
        title="Invite:",
		description="Get the bot's invite link [here](https://discord.com/api/oauth2/authorize?client_id=1003247499911376956&permissions=414464723008&scope=bot%20applications.commands).",
		color=0x2f3136
	)
    await ctx.respond(embed=embed)

#vote command
@bot.command
@lightbulb.command("vote", "Get the link to vote at top.gg.")
@lightbulb.implements(lightbulb.SlashCommand)
async def vote(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    embed = hikari.Embed(
		title="Vote:",
		description="Click [here](https://top.gg/bot/1003247499911376956/vote) to vote on top.gg. Thank you!",
		color=0x2f3136
    )
    await ctx.respond(embed=embed)

#support command
@bot.command
@lightbulb.command("support", "Invite to join the support server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def support(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    embed = hikari.Embed(
        title="Support:",
		description="Click [here](https://discord.com/invite/xNb8mpySK8) to join the support server.",
		color=0x2f3136
	)
    await ctx.respond(embed=embed)

#donate command
@bot.command
@lightbulb.command("donate", "Donate to support Anicord.")
@lightbulb.implements(lightbulb.SlashCommand)
async def donate(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    embed = hikari.Embed(
        title="Donate:",
        description="[Buy me a coffee](https://www.buymeacoffee.com/azael) to keep Anicord alive. Thank you! :)",
		color=0x2f3136
	)
    await ctx.respond(embed=embed)

#more command
@bot.command
@lightbulb.command("more", "Check out more bots from me.")
@lightbulb.implements(lightbulb.SlashCommand)
async def more(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    embed = hikari.Embed(
        title="More:",
        description="Click [here](https://top.gg/user/67067136345571328) to check out more bots from me.",
        color=0x2f3136
    )
    await ctx.respond(embed=embed)

#error handling
@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond("I couldn't find what you were looking for.")
        raise event.exception

    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"`/{event.context.command.name}` is on cooldown. Retry in `{exception.retry_after:.0f}` seconds. ⏱️ \n API commands are ratelimited to prevent spam abuse which could bring the bot down. \n To avoid cooldowns, become a member at https://www.buymeacoffee.com/azael.")
    else:
        raise exception

bot.run()
