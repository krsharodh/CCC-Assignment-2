let baseURL = "http://127.0.0.1:5000/api"
if (process.env.NODE_ENV === 'production') {
    baseURL = `${process.env.REACT_APP_PROD_URL}:${process.env.REACT_APP_PORT_NUMBER}/api`;
};


const GetCities = async () => {
    const response = await fetch(`${baseURL}/getCities`);
    const responseJson = await response.json();
    return responseJson;
}

const GetCovidGraph1Data = async () => {
    const response = await fetch(`${baseURL}/covid/getGraph1Data`);
    let responseJson = await response.json();
    return responseJson;
}

const GetCovidGraph2Data = async (city) => {
    const url = new URL(`${baseURL}/covid/getGraph2Data`)
    const params = { city: city }
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
    const response = await fetch(url);
    const responseJson = await response.json();
    return responseJson;
}

const GetCovidTopicsData = async () => {
    const response = await fetch(`${baseURL}/covid/words_cloud`);
    const responseJson = await response.json();
    return responseJson;
}

const GetCovidTweetByWord = async (word) => {
    const response = await fetch(`${baseURL}/covid/get_tweet_by_word`, 
    {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({'word':word.text
        })
    });
    const responseJson = await response.json();
    return responseJson;
}

const GetCovidHashtagsData = async () => {
    const response = await fetch(`${baseURL}/covid/hashtag/words_cloud`);
    const responseJson = await response.json();
    return responseJson;
}

const GetCovidTweetByHashtag = async (word) => {
    const response = await fetch(`${baseURL}/covid/hashtag/get_tweet_by_word`, 
    {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({'word':word.text
        })
    });
    const responseJson = await response.json();
    return responseJson;
}

const GetVaccineGraph1Data = async () => {
    const response = await fetch(`${baseURL}/vaccine/getGraph1Data`);
    let responseJson = await response.json();
    return responseJson;
}

const GetVaccineGraph2Data = async () => {
    const response = await fetch(`${baseURL}/vaccine/sentiment_trend`);
    let responseJson = await response.json();
    return responseJson;
}

const GetVaccineGraph3Data = async () => {
    const response = await fetch(`${baseURL}/vaccine/words_cloud`);
    let responseJson = await response.json();
    return responseJson;
}

const GetVaccineGraph4Data = async () => {
    const response = await fetch(`${baseURL}/vaccine/hashtag/words_cloud`);
    let responseJson = await response.json();
    return responseJson;
}

const GetVaccineTweetByWord = async (word) => {
    const response = await fetch(`${baseURL}/vaccine/get_tweet_by_word`, 
    {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({'word':word.text
        })
    });
    const responseJson = await response.json();
    return responseJson;
}

const GetVaccineTweetByHashtag = async (word) => {
    const response = await fetch(`${baseURL}/vaccine/hashtag/get_tweet_by_word`, 
    {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({'word':word.text
        })
    });
    const responseJson = await response.json();
    return responseJson;
}

const GetJobGraph1Data = async () => {
    const response = await fetch(`${baseURL}/job-keeper/getGraph1Data`);
    let responseJson = await response.json();
    return responseJson;
}

const GetJobGraph2Data = async () => {
    const response = await fetch(`${baseURL}/job-keeper/getGraph2Data`);
    let responseJson = await response.json();
    return responseJson;
}

const GetJobGraph3Data = async () => {
    const response = await fetch(`${baseURL}/job-keeper/getGraph3Data`);
    let responseJson = await response.json();
    return responseJson;
}


export {
    GetCities,

    GetCovidGraph1Data,
    GetCovidGraph2Data,
    GetCovidTopicsData,
    GetCovidHashtagsData,

    GetVaccineGraph1Data,
    GetVaccineGraph2Data,
    GetVaccineGraph3Data,
    GetVaccineGraph4Data,

    GetJobGraph1Data,
    GetJobGraph2Data,
    GetJobGraph3Data,
    GetCovidTweetByWord,
    GetCovidTweetByHashtag,
    GetVaccineTweetByWord,
    GetVaccineTweetByHashtag
};
