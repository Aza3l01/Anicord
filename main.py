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

prem_users = ["364400063281102852"]

#anime
@bot.command
@lightbulb.add_cooldown(length=20, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("name", "Anime")
@lightbulb.command("anisearch", "Look up an anime.", auto_defer=True)
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
@lightbulb.command("mangasearch", "Look up a manga.", auto_defer=True)
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
    posts = [post for post in sub.hot(limit=50)]
    random_post = random.choice(posts)
    
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
@lightbulb.add_cooldown(length = 1, uses = 1, bucket = lightbulb.UserBucket)
@lightbulb.option("name", "Anime")
@lightbulb.command("aniextended", "Receive search queries to choose for a more detailed experience.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def aniextended(ctx: lightbulb.Context) -> None:
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    if any(word in str(ctx.author.id) for word in prem_users):
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

        await ctx.respond("/aniextended is currectly unavailable but will be updated soon, visit the [support server](https://discord.com/invite/xNb8mpySK8) for updates.")
    else:
        await ctx.respond("/aniextended is currectly unavailable but will be updated soon, visit the [support server](https://discord.com/invite/xNb8mpySK8) for updates.")

#help command
@bot.command
@lightbulb.command("help", "Get help")
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    await bot.rest.create_message(1013474210242375741, f"`{ctx.command.name}` was used.")
    embed = hikari.Embed(
		title="__**Commands**__",
		description="**__Main:__** \n **/anisearch:** Look up an anime. \n **/mangasearch:** Look up a manga. \n **/animeme:** Get an anime meme. \n  **/aniextended:** Receive search queries to choose for a more detailed experience. \n \n **__Misc:__** \n **/invite:** Get the bot's invite link. \n **/vote:** Get the link to vote at top.gg. \n **/support:** Invite to join the support server. \n **/donate:** Donate to support Anicord. \n **/more:** Check out more bots from me.",
		color = 0x2f3136
	)
    embed.set_footer("Anicord is very new and under development. Feel free to join the support server, if you're having trouble using the bot :)")
    await ctx.respond(embed=embed)
    embed = embed = hikari.Embed(
		title = '',
			description = '**Thank you!** \n If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\nIf you want to help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership).',
			color = 0x2f3136
		)
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
    embed = embed = hikari.Embed(
		title = '',
			description = '**Thank you!** \n If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\nIf you want to help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership).',
			color = 0x2f3136
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
    embed = embed = hikari.Embed(
		title = '',
			description = '**Thank you!** \n If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\nIf you want to help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership).',
			color = 0x2f3136
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
    embed = embed = hikari.Embed(
		title = '',
			description = '**Thank you!** \n If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\nIf you want to help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership).',
			color = 0x2f3136
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
    embed = embed = hikari.Embed(
		title = '',
			description = '**Thank you!** \n If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\nIf you want to help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership).',
			color = 0x2f3136
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
    embed = embed = hikari.Embed(
		title = '',
			description = '**Thank you!** \n If you like using Anicord, consider [voting](https://top.gg/bot/1003247499911376956/vote) or leaving a [review](https://top.gg/bot/1003247499911376956).\nIf you want to help keep Anicord online, consider becoming a [member](https://buymeacoffee.com/azael/membership).',
			color = 0x2f3136
		)
    await ctx.respond(embed=embed)

#error handling
@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond("Something went wrong, please try again.😔")
        raise event.exception

    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"`/{event.context.command.name}` is on cooldown. Retry in `{exception.retry_after:.0f}` seconds. ⏱️ \n API commands are ratelimited to prevent spam abuse which could bring the bot down. \n To avoid cooldowns, become a member at https://www.buymeacoffee.com/azael.")
    else:
        raise exception

bot.run()