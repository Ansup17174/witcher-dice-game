const parseErrors = (error, setErrors) => {
    const errorObject = {};
        if (Array.isArray(error.response.data.detail)) {
            error.response.data.detail.forEach(error => {
                errorObject[error.loc[1]] = error.msg;
            });
            setErrors(errorObject);
        } else {
            setErrors(error.response.data);
        }
};

export default parseErrors;