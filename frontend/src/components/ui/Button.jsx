import classNames from 'classnames';
import propTypes from 'prop-types';

function Button({ onClick, className, children, variant = 'primary' }) {
  const classes = classNames({
    btn: true,
    'btn-primary': variant === 'primary',
    'btn-secondary': variant === 'secondary',
    'btn-icon': variant === 'icon'
  });

  return (
    <button onClick={onClick} className={classes + ' ' + className}>
      {children}
    </button>
  );
}

export default Button;

Button.propTypes = {
  children: propTypes.node,
  onClick: propTypes.func,
  className: propTypes.string,
  variant: propTypes.string
};

Button.defaultProps = {
  children: null,
  onClick: () => {},
  className: ''
};
