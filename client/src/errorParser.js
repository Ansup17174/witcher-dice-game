const parseErrors = (error, setErrors) => {
        if (Array.isArray(error.response.data.detail)) {
            const errorObject = {};
            error.response.data.detail.forEach(error => {
                errorObject[error.loc[1]] = error.msg;
            });
            setErrors(errorObject);
        } else {
            setErrors(error.response.data);
        }
};

export default parseErrors;