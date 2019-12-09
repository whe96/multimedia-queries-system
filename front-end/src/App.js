import React from 'react';

import './App.css';

import QueryBlock from "./QueryBlock";
import ResultBlock from "./ResultBlock";

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            index: 0,
            currentQuery: '',
            ratios: ['1', '1', '1', '1'],
            resultData: null
        };
        this.folders = [];

        this.handleQueryChange = this.handleQueryChange.bind(this);
        this.handleRatiosChange = this.handleRatiosChange.bind(this);
        this.requestData = this.requestData.bind(this);

        this.getQueriesFolder();
    }

    async getQueriesFolder() {
        const response = await fetch("http://localhost:5000/queries");
        const myJson = await response.json();
        this.folders =  myJson['folders'];
        this.setState({
            currentQuery: myJson['folders'][0]
        });
    }

    handleQueryChange(event) {
        this.setState({
            index: 0,
            currentQuery: event.target.id
        });
    }

    handleRatiosChange(event) {
        let name = event.target.name;
        let newRatios = [...this.state.ratios];
        let index;
        if (name === 'color') {
            index = 0;
        } else if (name === 'motion') {
            index = 1;
        } else if (name === 'sound') {
            index = 2;
        } else {
            index = 3;
        }
        newRatios[index] = event.target.value;
        this.setState({ratios: newRatios});
    }

    async requestData() {
        let url = "http://localhost:5000/results/" + this.state.currentQuery
            + "/" + this.state.ratios[0] + "/" + this.state.ratios[1]
            + "/" + this.state.ratios[2] + "/" + this.state.ratios[3];

        const response = await fetch(url);
        const resultData = await response.json();
        this.setState({
            index: this.state.index + 1,
            resultData: resultData
        });
    }

    render() {
        let resultBlock = (this.state.index > 0) ? (
            <div>
                <h3>Result</h3>
                <hr />
                <ResultBlock key={this.state.index} resultData={this.state.resultData}/>
            </div>) : null;

        return (
            <div className="App">
                <QueryBlock
                    folders={this.folders}
                    currentQuery={this.state.currentQuery}
                    ratios={this.state.ratios}
                    onQueryChange={this.handleQueryChange}
                    onRatiosChange={this.handleRatiosChange}
                    onRequestData={this.requestData}
                />
                {resultBlock}
            </div>
        );
    }
}

export default App;
