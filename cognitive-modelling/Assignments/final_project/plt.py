def plot_data(df):
    df = df[df["Main"] == True]
#     df = df[df["Block"].isin(["Short Uniform", "Long Uniform", "Medium Uniform", "Medium spiked"])]
#     df = df.round({"int": 2})
    short = df[df["Block"] == "Short Uniform"]
    long = df[df["Block"] == "Long Uniform"]
    medium = df[df["Block"] == "Medium Uniform"]
    medium_spiked = df[df["Block"] == "Medium spiked"]

    su = short.groupby(["int"])["resp"].mean().reset_index()
    su["bias"] = su["resp"] - su["int"]

    lu = long.groupby(["int"])["resp"].mean().reset_index()
    lu["bias"] = lu["resp"] - lu["int"]

    mu = medium.groupby(["int"])["resp"].mean().reset_index()
    mu["bias"] = mu["resp"] - mu["int"]

    mp = medium_spiked.groupby(["int"])["resp"].mean().reset_index()
    mp["bias"] = mp["resp"] - mp["int"]
    
    fig = plt.figure()

    plt.subplot(2, 2, 1)
    plt.scatter(su["int"], su["bias"], s=10, c='r', marker="o", label='Short Uniform')

    plt.subplot(2, 2, 2)
    plt.plot(x, y)

    plt.subplot(2, 2, 3)
    plt.plot(x, y)

    plt.subplot(2, 2, 4)
    plt.plot(x, y)

    plt.show()

    x = range(100)
    y = range(100,200)
    fig = plt.figure(figsize = (10, 5))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    ax1.scatter(su["int"], su["bias"], s=10, c='r', marker="o", label='Short Uniform')
    ax1.scatter(lu["int"], lu["bias"], s=10, c='g', marker="o", label='Long Uniform')
    ax1.yaxis.set_label_position("right")
    ax1.yaxis.tick_right()
    ax1.axhline(y=0, color='gray', linestyle='-')
    ax1.legend(loc='upper left');
    ax1.xlabel("Physical Time Interval (ms)")
    ax1.ylabel("Response Bias (ms)")

    ax2.scatter(mu["int"], mu["bias"], s=10, c='r', marker="1", label='Medium Uniform')
    ax2.scatter(mp["int"], mp["bias"], s=10, c='g', marker="o", label='Medium Spiked')
    ax2.yaxis.set_label_position("right")
    ax2.yaxis.tick_right()
    ax2.axhline(y=0, color='gray', linestyle='-')
    ax2.legend(loc='upper left');
    ax2.xlabel("Physical Time Interval (ms)")
    ax2.ylabel("Response Bias (ms)")
    
    plt.show()