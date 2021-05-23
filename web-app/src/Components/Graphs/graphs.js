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
    CartesianGrid
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
                <Bar dataKey="percentage" fill="#ff6361" stackId="a">
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
                <XAxis hide dataKey="name" />
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

const JobGraph = ({ data }) => {

    const renderCustomizedLabel = (props) => {
        const { content, ...rest } = props;
        return <Label {...rest} fontSize="12" fill="white" fontWeight="Bold" />;
    };

    return (
        <ResponsiveContainer height={250} width={"100%"}>
            <BarChart
                layout="vertical"
                data={data}
                margin={{ left: 10, right: 10 }}
                stackOffset="expand"
            >
                <XAxis hide type="number" />
                <YAxis
                    type="category"
                    dataKey="city"
                    stroke="black"
                    fontSize="12"
                />
                <Tooltip />
                <Bar dataKey="metioned_jobkeeper" fill="#ff6361" stackId="a">
                    <LabelList
                        dataKey="metioned_jobkeeper"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar>
                <Bar dataKey="median_weekly_personal_income" fill="#82ba7f" stackId="a">
                    <LabelList
                        dataKey="median_weekly_personal_income"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar>
            </BarChart>
        </ResponsiveContainer>
    );
}


export { CovidGraph1, CovidGraph2, Wordcloud, JobGraph };