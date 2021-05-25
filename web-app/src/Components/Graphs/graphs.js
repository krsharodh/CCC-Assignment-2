import {
    BarChart,
    Bar,
    LineChart,
    Line,
    XAxis,
    YAxis,
    ResponsiveContainer,
    Tooltip,
    Label,
    LabelList,
    Legend,
    CartesianGrid,
    ComposedChart,
    Area,
    ReferenceLine
} from "recharts";
import ReactWordcloud from 'react-wordcloud';
import { select } from "d3-selection";


const CovidGraph1 = ({ data }) => {

    const renderCustomizedLabel = (props) => {
        const { content, ...rest } = props;
        return <Label {...rest} fontSize="12" fill="white" fontWeight="Bold" value={`${rest.value} %`} />;
    };

    return (
        <ResponsiveContainer height={250} width={"100%"}>
            <BarChart
                layout="vertical"
                data={data}
                margin={{ left: 10, right: 10 }}
            >
                <XAxis hide type="number" />
                <YAxis
                    type="category"
                    dataKey="city"
                    stroke="black"
                    fontSize="12"
                />
                <Tooltip />
                <Bar dataKey="percentage" fill="#ff6827" stackId="a">
                    <LabelList
                        dataKey="percentage"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar>
                {/* <Bar dataKey="total_tweets" fill="#82ba7f" stackId="a">
                    <LabelList
                        dataKey="total_tweets"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar> */}
            </BarChart>
        </ResponsiveContainer>
    );
}

const CovidGraph2 = ({ data }) => {

    return (
        <ResponsiveContainer height={250} width={"100%"}>

            <LineChart data={data} margin={{ left: 10, right: 10 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis type="number" domain={[0, 'auto']} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="cases" stroke="#8884d8" dot={false} />
                <Line type="monotone" dataKey="tweets" stroke="#82ca9d" dot={false} />
            </LineChart>
        </ResponsiveContainer>
    );
}

const Wordcloud = ({ data }) => {
    const options = {
        colors: ['#1f77b4', '#ff7f0e', "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
        deterministic: false,
        fontFamily: "Times New Roman",
        fontSizes: [15, 100],
        fontStyle: "normal",
        fontWeight: "normal",
        padding: 1,
        rotations: 1,
        rotationAngles: [0, 90],
        scale: "log",
        spiral: "archimedean",
        transitionDuration: 1000,
        tooltipOptions: {
            allowHTML: true,
            appendTo: document.body,
            interactive: true,
            hideOnClick: false,
        }
    };

    // function getCallback(callback) {
    //     return function (word, event) {
    //         const isActive = callback !== "onWordMouseOut";
    //         const element = event.target;
    //         const text = select(element);
    //         text
    //             .transition()
    //             .attr("font-size", isActive ? word.size * 1.2 + 'px' : word.size + 'px')
    //         if (callback === 'onWordClick') {
    //             fetch("http://127.0.0.1:5000/covid/get_tweet_by_word", {
    //                 method: 'POST',
    //                 headers: {
    //                     "Content-Type": "application/json"
    //                 },
    //                 body: JSON.stringify({
    //                     'word': word.text
    //                 })
    //             }).then(res => res.json()).then(json => {
    //                 var element = document.getElementById(word.text)
    //                 var startIndex = json.data.toLowerCase().indexOf(word.text)
    //                 var endIndex = startIndex + word.text.length
    //                 if (element !== null) {
    //                     var innerHtml = ""
    //                     if (startIndex === 0) {
    //                         innerHtml = innerHtml + "<text><text style='color:#ff8000'>" + json.data.slice(0, endIndex) + "</text>" + json.data.slice(endIndex, json.data.length) + "</text>"
    //                     } else {
    //                         innerHtml = innerHtml + "<text>" + json.data.slice(0, startIndex) + "<text style='color: #ff8000'>" + json.data.slice(startIndex, endIndex) + "</text>" + json.data.slice(endIndex, json.data.length) + "</text>"
    //                     }
    //                     element.innerHTML = innerHtml
    //                 }
    //                 var content = document.getElementById(word.text + '_1')
    //                 if (content !== null) {
    //                     content.innerText = 'Example tweet with "' + word.text + '": '
    //                 }
    //             })
    //         }
    //     };
    // }

    // const callbacks = {
    //     getWordTooltip: (word) =>
    //         `<p id='${word.text + "_1"}'>The word "${word.text}" appears ${word.value} times.</p>
    //   <div id='${word.text}'></div>`,
    //     onWordClick: getCallback('onWordClick'),
    //     onWordMouseOut: getCallback("onWordMouseOut"),
    //     onWordMouseOver: getCallback('onMouseOver')
    // };


    return <ReactWordcloud words={data} options={options} />
}

const formatTicks = (tick) => {
    if (tick >= 1000) {
        return `${tick / 1000}K`
    }
    return tick
}

const JobGraph = ({ data, lineDataKey, yAxisLabel }) => {

    const renderCustomizedLabel = (props) => {
        const { content, ...rest } = props;
        return <Label {...rest} fontSize="12" fill="white" fontWeight="Bold" value={`${rest.value} %`} />;

    };

    return (
        <ResponsiveContainer height={250} width={"100%"}>
            <ComposedChart
                data={data}
                margin={{ left: 10, right: 10 }}
            >
                <XAxis
                    type="category"
                    dataKey="city"
                    stroke="black"
                    fontSize="12"
                    interval={0}
                />

                <YAxis
                    width={80}
                    yAxisId="left"
                    tick={{ fontSize: 10 }}
                    dataKey="percentage"
                >
                    <Label
                        value={"% of tweets"}
                        angle={-90}
                        position='outside'
                        fill='#676767'
                        fontSize={14}
                    />
                </YAxis>
                <YAxis
                    width={80}
                    yAxisId="right"
                    orientation="right"
                    tick={{ fontSize: 10, }}
                    dataKey={lineDataKey}
                    tickFormatter={tick => formatTicks(tick)}
                >
                    <Label
                        value={yAxisLabel}
                        angle={-90}
                        position='outside'
                        fill='#676767'
                        fontSize={14}
                    />
                </YAxis>
                <Tooltip />
                <Bar dataKey="percentage" fill="#ff6827" stackId="a" yAxisId="left">
                    <LabelList
                        dataKey="percentage"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar>
                <Line
                    type="monotone"
                    dataKey={lineDataKey}
                    stroke="#8884d8"
                    yAxisId="right"
                />
            </ComposedChart>
        </ResponsiveContainer>
    );
}

const formatDateTicks = (tick) => {
    var date = new Date(tick)
    var dd = date.getDate()
    var mm = date.getMonth() + 1
    var yy = date.getFullYear()
    return dd + '/' + mm + '/' + yy.toString().slice(2, 4)
}

const SentimentAnalysis = ({ data }) => {
    return (
        <>
            <p style={{ 'text-align': "center", 'font-size': '22px', "margin-top": '20px' }}>
                Sentiment Score of Vaccine-Related Tweets Over Time
            </p>
            <ResponsiveContainer height={500} width={"100%"}>
                <ComposedChart
                    margin={{
                        top: 20,
                        right: 20,
                        bottom: 20,
                        left: 20,
                    }}
                    data={data}
                >
                    <CartesianGrid stroke="#f5f5f5" />
                    <XAxis dataKey="date" interval={5}
                        tickFormatter={tick => formatDateTicks(tick)}
                    />
                    <YAxis type="number" domain={[-0.8, 0.8]} />
                    <Tooltip />
                    <Legend />
                    <Area type="monotone" name="80% confidence band" dataKey="range" fill="#8884d8" stroke="#8884d8" fillOpacity={0.3} strokeOpacity={0.5} />
                    <ReferenceLine y={0} stroke="red" strokeDasharray="5 5" />
                    <Line type="monotone" name="avg_sentiment_score" dataKey="value" stroke="#8884d8" strokeWidth={3} />
                </ComposedChart>
            </ResponsiveContainer>
        </>
    )
}

const VaccineBarGraph = ({ data, lineDataKey, yAxisLabel }) => {

    const renderCustomizedLabel = (props) => {
        const { content, ...rest } = props;
        return <Label {...rest} fontSize="12" fill="white" fontWeight="Bold" value={`${rest.value}`} />;

    };

    return (
        <ResponsiveContainer height={250} width={"100%"}>
            <ComposedChart
                data={data}
                margin={{ left: 10, right: 10 }}
            >
                <XAxis
                    type="category"
                    dataKey="city"
                    stroke="black"
                    fontSize="12" />

                <YAxis
                    width={80}
                    yAxisId="left"
                    tick={{ fontSize: 10 }}
                    dataKey="value"
                >
                    <Label
                        value={"avg sentiment score"}
                        angle={-90}
                        position='outside'
                        fill='#676767'
                        fontSize={14}
                    />
                </YAxis>
                <YAxis
                    width={80}
                    yAxisId="right"
                    orientation="right"
                    tick={{ fontSize: 10, }}
                    dataKey={lineDataKey}
                    tickFormatter={tick => formatTicks(tick)}
                >
                    <Label
                        value={yAxisLabel}
                        angle={-90}
                        position='outside'
                        fill='#676767'
                        fontSize={14}
                    />
                </YAxis>
                <Tooltip />
                <Bar dataKey="value" fill="#ff9d2f" stackId="a" yAxisId="left">
                    <LabelList
                        dataKey="value"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar>
                <Line
                    type="linear"
                    dataKey={lineDataKey}
                    stroke="#8884d8"
                    strokeWidth={3}
                    yAxisId="right"
                />
            </ComposedChart>
        </ResponsiveContainer>
    );
}


export { CovidGraph1, CovidGraph2, Wordcloud, JobGraph, SentimentAnalysis, VaccineBarGraph };