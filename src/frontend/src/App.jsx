import React from 'react';

import { GetRequest } from './';

class App extends React.Component {
    render() {
        return (
            <div>
                <h3 className="p-3 text-center">All Datasets</h3>
                <GetRequest />
            </div>
        );
    }
}

export { App }; 