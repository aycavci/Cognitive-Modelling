def plot_data(df):
    df = df[df["Main"] == True]
    intervals = df[df["Block"].isin(["short", "long"])]
    intervals = intervals.round({"int": 2})
    short = intervals[intervals["Block"] == "Short Uniform"]
    long = intervals[intervals["Block"] == "Long Uniform"]
    medium = intervals[intervals["Block"] == "Medium Uniform"]
    medium_spiked = intervals[intervals["Block"] == "Medium Spiked"]

    su = short.groupby(["int"])["resp"].mean().reset_index() * 1000
    su["bias"] = su["resp"] - su["int"]

    lu = long.groupby(["int"])["resp"].mean().reset_index() * 1000
    lu["bias"] = lu["resp"] - lu["int"]

    mu = long.groupby(["int"])["resp"].mean().reset_index() * 1000
    mu["bias"] = mu["resp"] - mu["int"]

    mu = long.groupby(["int"])["resp"].mean().reset_index() * 1000
    mp["bias"] = mp["resp"] - mp["int"]

    x = range(100)
    y = range(100,200)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = fig.add_subplot(112)

    ax1.scatter(su["int"], su["bias"], s=10, c='r', marker="o", label='Short Uniform')
    ax1.scatter(lu["int"], lu["bias"], s=10, c='g', marker="o", label='Long Uniform')

    ax2.scatter(mu["int"], mu["bias"], s=10, c='r', marker="o", label='Medium Uniform')
    ax2.scatter(mp["int"], mp["bias"], s=10, c='g', marker="o", label='Medium Spiked')
    
    plt.axhline(y=0, color='gray', linestyle='-')
    plt.legend(loc='upper left');
    plt.xlabel("Physical Time Interval (ms)")
    plt.ylabel("Response Bias (ms)")
    plt.show()