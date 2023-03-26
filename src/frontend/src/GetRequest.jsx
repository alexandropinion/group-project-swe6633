import React from 'react';

class GetRequest extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            totalReactPackages: null
        };
    }

    componentDidMount() {
        // Simple GET request using fetch
        fetch('http://127.0.0.1:8000/user-read-datasets')
            .then(response => response.json())
            .then(data => this.setState({ totalReactPackages: response }));
    }

    render() {
        const { totalReactPackages } = this.state;
        return (
            <div className="card text-center m-3">
                <h5 className="card-header">Example</h5>
                <div className="card-body">
                    Items: {totalReactPackages}
                </div>
            </div>
        );
    }
}

export { GetRequest }; 