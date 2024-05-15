import { render, fireEvent } from '@testing-library/vue'
import { mount } from '@vue/test-utils'
import HomePage from '@/components/HomePage.vue'
import sinon from 'sinon'
import jest from 'jest'


test('renders initial text correctly', async () => {
  const { getByText } = render(HomePage);
  // Assert initial text is rendered
  getByText('Check your medication here:');
});

test('renders initial image correctly', async () => {
  const { getElementById } = render(HomePage)
  // Assert initial image is rendered
  const imgElement = document.getElementById('medication')
  expect(imgElement).toBeTruthy()
})

test('renders UPLOAD FILE label correctly', async () => {
  const { getByLabelText } = render(HomePage);

  // Assert UPLOAD FILE label is rendered
  const labelElement = getByLabelText('UPLOAD FILE');
  expect(labelElement).to.exist;
});

test('renders SUBMIT button correctly', async () => {
  const { getByText } = render(HomePage);

  // Assert SUBMIT button is rendered
  getByText('SUBMIT');
});

test('loading spinner is not rendered initially', async () => {
  const { queryByRole } = render(HomePage);

  // Assert loading spinner is not rendered initially
  expect(queryByRole('status')).toBeNull();
});

test('file input change updates image display', async () => {
  const { getByLabelText } = render(HomePage)

  // Mock a file selection
  const file = new File(['(⌐□_□)'], 'test.png', { type: 'image/png' })
  await fireEvent.change(getByLabelText('UPLOAD FILE'), { target: { files: [file] } })

})


// test('updates step when handleSubmit is called', async () => {
//   const wrapper = mount(HomePage);
  
//   // Simulate uploading a file
//   const file = new File(['dummy content'], 'test.png', { type: 'image/png' });
//   const inputFile = wrapper.find('input[type="file"]').element;
//   inputFile.files = [file];
  
//   // Manually trigger the change event to simulate file selection
//   await wrapper.find('input[type="file"]').trigger('change');
  
//   // Call handleSubmit function
//   await wrapper.vm.handleSubmit();
  
//   // Assert the updated value of 'step'
//   expect(wrapper.vm.step).toBe(2);
// });

// test('reupload function changes step back to 1 and success to false', async () => {
//   const { getByText, getByTestId } = render(HomePage)

//   // Set step to 2 and success to true
//   await fireEvent.click(getByText('SUBMIT'))

//   // Click the reupload button
//   await fireEvent.click(getByTestId('reupload-button'))

//   // Assert step and success are updated
//   expect(getByTestId('step-value')).toHaveTextContent('1')
//   expect(getByTestId('success-value')).toHaveTextContent('false')
// })



