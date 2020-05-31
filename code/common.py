class common:
      def display_images(data):
              img_data = list(data.T.to_dict().values())
              #img_data = list(data)
              f, ax = plt.subplots(1,3, figsize=(16,18))
              for i,data_row in enumerate(img_data):
                    imageName = data_row['patientId']+'.dcm'
                    imagePath = os.path.join(project_path+"/dataset/stage_2_train_images/",imageName)
                    data_row_img = dcm.dcmread(imagePath)
                    ax[i%3].imshow(data_row_img.pixel_array, cmap=plt.cm.bone) 
                    ax[i%3].axis('off')
                    ax[i%3].set_title('ID: {}\nClass: {}'.format(
                        data_row['patientId'], data_row['class']))
              plt.show()

      def display_images_with_boxes(data):
              img_data = list(data.T.to_dict().values())
              f, ax = plt.subplots(1,3, figsize=(16,18))
              for i,data_row in enumerate(img_data):
                    imageName = data_row['patientId']+'.dcm'
                    imagePath = os.path.join(project_path+"/dataset/stage_2_train_images/",imageName)
                    data_row_img = dcm.dcmread(imagePath)
                    ax[i%3].imshow(data_row_img.pixel_array, cmap=plt.cm.bone) 
                    ax[i%3].axis('off')
                    ax[i%3].set_title('ID: {}\nClass: {}'.format(
                        data_row['patientId'], data_row['class']))
                    rows = train_class_df[train_class_df['patientId']==data_row['patientId']]
                    box_data = list(rows.T.to_dict().values())
                    for j, row in enumerate(box_data):
                        ax[i%3].add_patch(Rectangle(xy=(row['x'], row['y']),
                            width=row['width'],height=row['height'], 
                            linewidth=1,edgecolor='r',facecolor='none'))   
              plt.show()

      def collect_metadata(data, location):
              dcm_columns = None

              for n, pid in enumerate(data['patientId'].unique()):
                    imageName = pid+'.dcm'
                    imagePath = os.path.join(project_path + location, imageName)
                    dcm_data = dcm.read_file(imagePath)
                    """ 
                    if not dcm_columns:
                        dcm_columns = dcm_data.dir()

                    for col in dcm_columns:
                        if col in ["PatientAge", "PatientSex", "ViewPosition"]:
                              value = dcm_data.data_element(col).value
                              index = data[data['patientId'] == pid].index
                              data.loc[index, col] = value
                      """ 
                    index = data[data['patientId'] == pid].index
                    data.loc[index, "PatientAge"] = dcm_data.data_element("PatientAge").value
                    data.loc[index, "PatientSex"] = dcm_data.data_element("PatientSex").value
                    data.loc[index, "ViewPosition"] = dcm_data.data_element("ViewPosition").value
                    del dcm_data